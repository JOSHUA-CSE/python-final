from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Course, Quiz, Question, Option, Discussion, Comment, Resource
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            from django.contrib.auth import login
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard') # Redirect to dashboard after signup
    else:
        form = UserCreationForm()
    return render(request, 'courses/signup.html', {'form': form})

@login_required
def dashboard(request):
    enrolled_courses = request.user.courses_enrolled.all()
    all_courses = Course.objects.all()
    available_courses = [course for course in all_courses if course not in enrolled_courses]

    context = {
        'enrolled_courses': enrolled_courses,
        'available_courses': available_courses,
    }
    return render(request, 'courses/dashboard.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if the user is an instructor for this course
    is_instructor = request.user in course.instructors.all()

    if request.method == 'POST':
        # Handle resource upload only if the user is an instructor
        if is_instructor and 'resource_file' in request.FILES:
            title = request.POST.get('title', '')
            description = request.POST.get('description', '')
            uploaded_file = request.FILES['resource_file']

            # Basic file type validation (optional, can be enhanced)
            allowed_types = ['pdf', 'pptx', 'mp4', 'docx', 'zip']
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension not in allowed_types:
                 messages.error(request, 'Invalid file type. Allowed types: pdf, pptx, mp4, docx, zip.')
            else:
                try:
                    Resource.objects.create(
                        course=course,
                        title=title,
                        description=description,
                        file=uploaded_file,
                        uploaded_by=request.user
                    )
                    messages.success(request, 'Resource uploaded successfully!')
                except Exception as e:
                    messages.error(request, f'Error uploading resource: {e}')

            # Redirect back to the course detail page to show updated resources
            return redirect('course_detail', course_id=course_id)

        # Handle existing POST logic (e.g., adding comments)
        if 'content' in request.POST:
            main_discussion = course.discussions.first()
            if main_discussion:
                content = request.POST.get('content')
                if content:
                    Comment.objects.create(
                        discussion=main_discussion,
                        content=content,
                        author=request.user
                    )
                    messages.success(request, 'Comment added successfully!')
            return redirect('course_detail', course_id=course_id)

    quizzes = course.quizzes.all()
    discussions = course.discussions.all()
    # Get the main discussion (first one)
    main_discussion = course.discussions.first()
    comments = main_discussion.comments.all() if main_discussion else []
    
    # Fetch resources for this course
    resources = course.resources.all().order_by('-upload_date')

    context = {
        'course': course,
        'quizzes': quizzes,
        'discussions': discussions,
        'main_discussion': main_discussion,
        'comments': comments,
        'is_instructor': is_instructor, # Pass instructor status to template
        'resources': resources, # Pass resources to template
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'courses/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions
    })

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())
    total_questions = len(questions)
    current = int(request.GET.get('q', 1))
    if current < 1 or current > total_questions:
        current = 1
    question = questions[current-1]
    options = question.options.all()
    selected = None
    score = int(request.session.get(f'quiz_{quiz_id}_score', 0))
    answers = request.session.get(f'quiz_{quiz_id}_answers', {})

    if request.method == 'POST':
        selected = request.POST.get('option')
        answers[str(question.id)] = selected
        if selected and Option.objects.filter(id=selected, question=question, is_correct=True).exists():
            score += question.points
        request.session[f'quiz_{quiz_id}_score'] = score
        request.session[f'quiz_{quiz_id}_answers'] = answers
        if current < total_questions:
            return redirect(f"{reverse('take_quiz', args=[quiz.id])}?q={current+1}")
        else:
            final_score = score
            request.session[f'quiz_{quiz_id}_score'] = 0
            request.session[f'quiz_{quiz_id}_answers'] = {}
            return render(request, 'courses/quiz_result.html', {
                'quiz': quiz,
                'score': final_score,
                'total': sum(q.points for q in questions)
            })

    progress = int((current/total_questions)*100)
    return render(request, 'courses/take_quiz.html', {
        'quiz': quiz,
        'question': question,
        'options': options,
        'current': current,
        'total_questions': total_questions,
        'progress': progress
    })

@login_required
def discussion_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    discussions = course.discussions.all()
    return render(request, 'courses/discussion_list.html', {
        'course': course,
        'discussions': discussions
    })

@login_required
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    comments = discussion.comments.all()
    return render(request, 'courses/discussion_detail.html', {
        'discussion': discussion,
        'comments': comments
    })

@login_required
def add_comment(request, discussion_id):
    if request.method == 'POST':
        discussion = get_object_or_404(Discussion, id=discussion_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                discussion=discussion,
                content=content,
                author=request.user
            )
            messages.success(request, 'Comment added successfully!')
    return redirect('discussion_detail', discussion_id=discussion_id)

@login_required # Ensure user is logged in
@require_POST # Only allow POST requests
@csrf_protect # Protect against CSRF attacks
def enroll_course(request, course_id):
    """
    Handles user enrollment in a course via AJAX POST request.
    """
    try:
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # Check if the user is already enrolled to prevent duplication
        if user not in course.students.all():
            course.students.add(user)
            # Return a success JSON response
            return JsonResponse({'success': True, 'message': f'Successfully enrolled in {course.title}!'})
        else:
            # Return a failure JSON response if already enrolled
            return JsonResponse({'success': False, 'error': 'You are already enrolled in this course.'}, status=400) # Use 400 for bad request

    except Course.DoesNotExist:
        # Return a failure JSON response if course not found
        return JsonResponse({'success': False, 'error': 'Course not found.'}, status=404) # Use 404 for not found
    except Exception as e:
        # Return a generic failure JSON response for other errors
        return JsonResponse({'success': False, 'error': f'An unexpected error occurred: {str(e)}'}, status=500) # Use 500 for server error

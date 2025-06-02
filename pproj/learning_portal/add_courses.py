import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_portal.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Course, Quiz, Question, Discussion, Option

# Create a superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

# Get the admin user
admin_user = User.objects.get(username='admin')

# Sample courses data
courses_data = [
    {
        'title': 'Introduction to Python Programming',
        'description': 'Learn the fundamentals of Python programming language. Topics include variables, data types, control structures, functions, and basic object-oriented programming concepts.',
    },
    {
        'title': 'Web Development with Django',
        'description': 'Master web development using Django framework. Learn to build dynamic web applications, handle databases, and implement user authentication.',
    },
    {
        'title': 'Data Structures and Algorithms',
        'description': 'Study fundamental data structures and algorithms. Topics include arrays, linked lists, trees, sorting algorithms, and basic algorithm analysis.',
    },
    {
        'title': 'Database Management Systems',
        'description': 'Learn about database design, SQL, and database management. Topics include normalization, transactions, and database optimization.',
    },
    {
        'title': 'Computer Networks',
        'description': 'Study the fundamentals of computer networking. Learn about protocols, network architecture, and network security.',
    }
]

# Create courses
for course_data in courses_data:
    course, created = Course.objects.get_or_create(
        title=course_data['title'],
        defaults={
            'description': course_data['description'],
            'instructor': admin_user
        }
    )
    
    if created:
        print(f"Created course: {course.title}")
        
        # Create a sample quiz for each course
        quiz = Quiz.objects.create(
            course=course,
            title=f"{course.title} - Quiz 1",
            description=f"Basic assessment for {course.title}"
        )
        
        # Create sample questions for the quiz
        questions = [
            {
                'text': f"What is the main topic of {course.title}?",
                'correct_answer': 'Basic concepts and fundamentals',
                'points': 2
            },
            {
                'text': f"Why is {course.title} important?",
                'correct_answer': 'It provides essential knowledge for the field',
                'points': 2
            }
        ]
        
        for q_data in questions:
            Question.objects.create(
                quiz=quiz,
                text=q_data['text'],
                points=q_data['points']
            )
        
        # Create a sample discussion
        discussion = Discussion.objects.create(
            course=course,
            title=f"Welcome to {course.title}!",
            content=f"Welcome to the {course.title} course! Feel free to introduce yourself and share your expectations for this course.",
            author=admin_user
        )

# Additional instructor courses
instructor_courses = [
    {
        'title': 'Introduction to Artificial Intelligence',
        'description': 'Explore the basics of AI, including search algorithms, knowledge representation, and simple machine learning concepts. This course is perfect for beginners interested in how computers can simulate intelligent behavior.'
    },
    {
        'title': 'Front-End Web Development with HTML, CSS, and JavaScript',
        'description': 'Learn how to build beautiful and interactive websites from scratch. This course covers HTML for structure, CSS for styling, and JavaScript for interactivity, with hands-on projects.'
    },
    {
        'title': 'Introduction to Data Science with Python',
        'description': "Dive into data analysis, visualization, and basic machine learning using Python. You'll work with libraries like pandas, matplotlib, and scikit-learn to analyze real-world datasets."
    },
    {
        'title': 'Object-Oriented Programming in Java',
        'description': 'Master the principles of object-oriented programming using Java. Topics include classes, objects, inheritance, polymorphism, and interfaces, with practical coding exercises.'
    },
    {
        'title': 'Cybersecurity Fundamentals',
        'description': 'Understand the basics of cybersecurity, including common threats, cryptography, network security, and best practices for protecting digital information.'
    }
]

for course_data in instructor_courses:
    course, created = Course.objects.get_or_create(
        title=course_data['title'],
        defaults={
            'description': course_data['description'],
            'instructor': admin_user
        }
    )
    if created:
        print(f"Created instructor course: {course.title}")
        quiz = Quiz.objects.create(
            course=course,
            title=f"{course.title} - Quiz 1",
            description=f"Basic assessment for {course.title}"
        )
        questions = [
            {
                'text': f"What is the main topic of {course.title}?",
                'correct_answer': 'Basic concepts and fundamentals',
                'points': 2
            },
            {
                'text': f"Why is {course.title} important?",
                'correct_answer': 'It provides essential knowledge for the field',
                'points': 2
            }
        ]
        for q_data in questions:
            Question.objects.create(
                quiz=quiz,
                text=q_data['text'],
                points=q_data['points']
            )
        Discussion.objects.create(
            course=course,
            title=f"Welcome to {course.title}!",
            content=f"Welcome to the {course.title} course! Feel free to introduce yourself and share your expectations for this course.",
            author=admin_user
        )

# Add a quiz to every course if it doesn't have one
for course in Course.objects.all():
    if not course.quizzes.exists():
        quiz = Quiz.objects.create(
            course=course,
            title="General Quiz",
            description=f"A general quiz for {course.title}"
        )
        Question.objects.create(
            quiz=quiz,
            text="What is the main topic of this course?",
            points=1
        )
        Question.objects.create(
            quiz=quiz,
            text="Who is the instructor of this course?",
            points=1
        )
        print(f"Added quiz to course: {course.title}")
print("All courses now have at least one quiz!")

# Define sample questions and options for each course
course_quiz_data = {
    'Introduction to Python Programming': [
        {
            'text': 'What is Python?',
            'options': [
                {'text': 'A programming language', 'is_correct': True},
                {'text': 'A type of snake', 'is_correct': False},
                {'text': 'A web browser', 'is_correct': False},
                {'text': 'A database', 'is_correct': False},
            ]
        },
        {
            'text': 'Which keyword is used to define a function in Python?',
            'options': [
                {'text': 'def', 'is_correct': True},
                {'text': 'func', 'is_correct': False},
                {'text': 'function', 'is_correct': False},
                {'text': 'define', 'is_correct': False},
            ]
        },
        {
            'text': 'Which of the following is used to define a block of code in Python?',
            'options': [
                {'text': 'Curly braces {}', 'is_correct': False},
                {'text': 'Parentheses ()', 'is_correct': False},
                {'text': 'Indentation', 'is_correct': True},
                {'text': 'Keywords (like if, for, while)', 'is_correct': False},
            ]
        },
        {
            'text': 'What is the output of the following Python code?\n```python\nx = ["apple", "banana", "cherry"]\nprint(x[1])\n```',
            'options': [
                {'text': 'apple', 'is_correct': False},
                {'text': 'banana', 'is_correct': True},
                {'text': 'cherry', 'is_correct': False},
                {'text': 'Error', 'is_correct': False},
            ]
        },
        {
            'text': 'Which built-in function is used to iterate over a sequence while also keeping track of the index?',
            'options': [
                {'text': 'iter()', 'is_correct': False},
                {'text': 'enumerate()', 'is_correct': True},
                {'text': 'index()', 'is_correct': False},
                {'text': 'range()', 'is_correct': False},
            ]
        },
        {
            'text': 'Explain the difference between `list` and `tuple` in Python.',
            'options': [
                {'text': 'Lists are immutable, while tuples are mutable.', 'is_correct': False},
                {'text': 'Lists use () for declaration, while tuples use [].', 'is_correct': False},
                {'text': 'Lists are mutable, while tuples are immutable.', 'is_correct': True},
                {'text': 'There is no fundamental difference; they are interchangeable.', 'is_correct': False},
            ]
        },
        {
            'text': 'What is a generator in Python and how is it created?',
            'options': [
                {'text': 'A function that returns multiple values using the `return` keyword.', 'is_correct': False},
                {'text': 'An object that produces values on the fly using the `yield` keyword, created like a function.', 'is_correct': True},
                {'text': 'A class that generates random numbers.', 'is_correct': False},
                {'text': 'A decorator used to create singletons.', 'is_correct': False},
            ]
        },
    ],
    'Web Development with Django': [
        {
            'text': 'Django is a ___ framework.',
            'options': [
                {'text': 'Web', 'is_correct': True},
                {'text': 'Mobile', 'is_correct': False},
                {'text': 'Desktop', 'is_correct': False},
                {'text': 'Game', 'is_correct': False},
            ]
        },
        {
            'text': 'Which language is Django written in?',
            'options': [
                {'text': 'Python', 'is_correct': True},
                {'text': 'Java', 'is_correct': False},
                {'text': 'C++', 'is_correct': False},
                {'text': 'PHP', 'is_correct': False},
            ]
        },
        {
            'text': 'Which command creates a new Django app?',
            'options': [
                {'text': 'python manage.py startapp', 'is_correct': True},
                {'text': 'django-admin newapp', 'is_correct': False},
                {'text': 'python create app', 'is_correct': False},
                {'text': 'django new app', 'is_correct': False},
            ]
        },
    ],
    'Data Structures and Algorithms': [
        {
            'text': 'Which data structure uses FIFO order?',
            'options': [
                {'text': 'Queue', 'is_correct': True},
                {'text': 'Stack', 'is_correct': False},
                {'text': 'Tree', 'is_correct': False},
                {'text': 'Graph', 'is_correct': False},
            ]
        },
        {
            'text': 'What is the time complexity of binary search?',
            'options': [
                {'text': 'O(log n)', 'is_correct': True},
                {'text': 'O(n)', 'is_correct': False},
                {'text': 'O(n^2)', 'is_correct': False},
                {'text': 'O(1)', 'is_correct': False},
            ]
        },
        {
            'text': 'Which of these is not a sorting algorithm?',
            'options': [
                {'text': 'Bubble sort', 'is_correct': False},
                {'text': 'Quick sort', 'is_correct': False},
                {'text': 'Merge sort', 'is_correct': False},
                {'text': 'Linear search', 'is_correct': True},
            ]
        },
        {
            'text': 'In Big O notation, what does O(1) represent?',
            'options': [
                {'text': 'Linear time complexity', 'is_correct': False},
                {'text': 'Logarithmic time complexity', 'is_correct': False},
                {'text': 'Constant time complexity', 'is_correct': True},
                {'text': 'Quadratic time complexity', 'is_correct': False},
            ]
        },
        {
            'text': 'Which data structure uses the Last-In, First-Out (LIFO) principle?',
            'options': [
                {'text': 'Queue', 'is_correct': False},
                {'text': 'Stack', 'is_correct': True},
                {'text': 'Linked List', 'is_correct': False},
                {'text': 'Tree', 'is_correct': False},
            ]
        },
        {
            'text': 'What is the average time complexity for searching an element in a balanced Binary Search Tree (BST)?',
            'options': [
                {'text': 'O(1)', 'is_correct': False},
                {'text': 'O(log n)', 'is_correct': True},
                {'text': 'O(n)', 'is_correct': False},
                {'text': 'O(n log n)', 'is_correct': False},
            ]
        },
        {
            'text': 'Describe the main difference between a depth-first search (DFS) and a breadth-first search (BFS) traversal on a graph.',
            'options': [
                {'text': 'DFS uses a queue, while BFS uses a stack.', 'is_correct': False},
                {'text': 'DFS explores as far as possible along each branch before backtracking, while BFS explores neighbor nodes first.', 'is_correct': True},
                {'text': 'DFS is only for directed graphs, while BFS is for undirected graphs.', 'is_correct': False},
                {'text': 'BFS is always faster than DFS.', 'is_correct': False},
            ]
        },
        {
            'text': 'Explain the concept of dynamic programming and when it is typically applied.',
            'options': [
                {'text': 'A technique for writing programs that can change their behavior at runtime, applied in object-oriented design.', 'is_correct': False},
                {'text': 'An algorithmic technique that solves problems by breaking them down into simpler subproblems and storing the results to avoid recomputing, applied to problems with overlapping subproblems and optimal substructure.', 'is_correct': True},
                {'text': 'A method for managing database transactions, applied in concurrent systems.', 'is_correct': False},
                {'text': 'A sorting algorithm for large datasets.', 'is_correct': False},
            ]
        },
    ],
    'Database Management Systems': [
        {
            'text': 'Which language is used to query databases?',
            'options': [
                {'text': 'SQL', 'is_correct': True},
                {'text': 'HTML', 'is_correct': False},
                {'text': 'CSS', 'is_correct': False},
                {'text': 'XML', 'is_correct': False},
            ]
        },
        {
            'text': 'Which is a relational database?',
            'options': [
                {'text': 'MySQL', 'is_correct': True},
                {'text': 'MongoDB', 'is_correct': False},
                {'text': 'Redis', 'is_correct': False},
                {'text': 'Neo4j', 'is_correct': False},
            ]
        },
        {
            'text': 'What does ACID stand for?',
            'options': [
                {'text': 'Atomicity, Consistency, Isolation, Durability', 'is_correct': True},
                {'text': 'Access, Control, Integrity, Data', 'is_correct': False},
                {'text': 'Array, Column, Index, Data', 'is_correct': False},
                {'text': 'None of the above', 'is_correct': False},
            ]
        },
    ],
    'Computer Networks': [
        {
            'text': 'What does TCP stand for?',
            'options': [
                {'text': 'Transmission Control Protocol', 'is_correct': True},
                {'text': 'Transfer Control Protocol', 'is_correct': False},
                {'text': 'Transmission Communication Protocol', 'is_correct': False},
                {'text': 'Transfer Communication Protocol', 'is_correct': False},
            ]
        },
        {
            'text': 'Which device forwards data packets between networks?',
            'options': [
                {'text': 'Router', 'is_correct': True},
                {'text': 'Switch', 'is_correct': False},
                {'text': 'Hub', 'is_correct': False},
                {'text': 'Repeater', 'is_correct': False},
            ]
        },
        {
            'text': 'What is the main function of DNS?',
            'options': [
                {'text': 'Translates domain names to IP addresses', 'is_correct': True},
                {'text': 'Encrypts data', 'is_correct': False},
                {'text': 'Routes packets', 'is_correct': False},
                {'text': 'Blocks spam', 'is_correct': False},
            ]
        },
    ],
}

# Add or update quizzes with these questions and options
for course_title, questions in course_quiz_data.items():
    course = Course.objects.filter(title__icontains=course_title).first()
    if not course:
        continue
    quiz = course.quizzes.first()
    if not quiz:
        quiz = Quiz.objects.create(course=course, title=f'{course.title} - Quiz', description=f'Quiz for {course.title}')
    # Remove old questions for a clean slate
    quiz.questions.all().delete()
    for qd in questions:
        q = Question.objects.create(quiz=quiz, text=qd['text'], points=1)
        for opt in qd['options']:
            Option.objects.create(question=q, text=opt['text'], is_correct=opt['is_correct'])
    print(f'Added/updated quiz for course: {course.title}')

print('All main courses now have realistic quizzes and options!')

for question in Question.objects.all():
    if question.options.count() == 0:
        Option.objects.create(question=question, text='Correct Answer', is_correct=True)
        Option.objects.create(question=question, text='Wrong Answer 1', is_correct=False)
        Option.objects.create(question=question, text='Wrong Answer 2', is_correct=False)
        Option.objects.create(question=question, text='Wrong Answer 3', is_correct=False)
        print(f"Added options to question: {question.text}")
print("All questions now have options!")

print("Sample courses, quizzes, and discussions have been created successfully!")
print("Instructor courses have been added!")

# Add quizzes and questions from course_quiz_data
print("Adding specific quizzes and questions...")
for course_title, questions_data in course_quiz_data.items():
    try:
        course = Course.objects.get(title=course_title)
        # Find or create a quiz for this course. You might want a more specific quiz title.
        quiz, created = Quiz.objects.get_or_create(
            course=course,
            title=f"{course.title} - Technical Quiz", # Using a more specific title
            defaults={'description': f"Technical questions for {course.title}"}
        )
        if created:
            print(f" Created technical quiz for {course.title}")

        for q_data in questions_data:
            # Check if question already exists to prevent duplicates on rerun
            question, created = Question.objects.get_or_create(
                quiz=quiz,
                text=q_data['text'],
                defaults={'points': 1} # Assigning a default point value
            )
            if created:
                print(f"  Added question: {question.text[:50]}...")
                for opt_data in q_data['options']:
                    Option.objects.create(
                        question=question,
                        text=opt_data['text'],
                        is_correct=opt_data['is_correct']
                    )
    except Course.DoesNotExist:
        print(f" Course '{course_title}' not found. Skipping questions for this course.")
    except Exception as e:
        print(f" An error occurred while adding questions for '{course_title}': {e}")

print("Finished adding specific quizzes and questions.")

# End of add_courses.py script 
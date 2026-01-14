from core.models import UserProfile

def create_user_profile(form_data):
    required_fields = [
        'name', 'age', 'current_grade',
        'academic_subjects', 'grades',
        'preferred_work_environment'
    ]

    for field in required_fields:
        if not form_data.get(field):
            raise ValueError(f"{field.replace('_', ' ').title()} is required.")

    raw_subjects = form_data['academic_subjects']

    if ',' not in raw_subjects:
        raise ValueError(
            "Academic subjects must be comma-separated (e.g., Maths, Physics)."
        )

    academic_subjects = [
        s.strip() for s in raw_subjects.split(',')
        if s.strip()
    ]

    if not academic_subjects:
        raise ValueError("Academic subjects cannot be empty.")

    grades_dict = {}
    grade_pairs = form_data['grades'].split(',')

    for pair in grade_pairs:
        if ':' not in pair:
            raise ValueError(
                "Grades must follow the format: subject: grade (e.g., maths: A)"
            )

        subject, grade = pair.split(':', 1)
        subject, grade = subject.strip(), grade.strip()

        if not subject or not grade:
            raise ValueError(
                "Grades must contain both subject and grade."
            )

        grades_dict[subject] = grade

    interests = [
        s.strip() for s in form_data.get('interests', '').split(',')
        if s.strip()
    ]

    hobbies = [
        s.strip() for s in form_data.get('hobbies', '').split(',')
        if s.strip()
    ]

    return UserProfile(
        name=form_data['name'],
        age=int(form_data['age']),
        current_grade=form_data['current_grade'],
        academic_subjects=academic_subjects,
        grades=grades_dict,
        interests=interests,
        hobbies=hobbies,
        preferred_work_environment=form_data['preferred_work_environment'],
        career_goals=form_data.get('career_goals'),
        location_preference=form_data.get('location_preference', 'Any'),
        budget_range=form_data.get('budget_range', 'Medium')
    )

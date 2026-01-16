from app.models import UserProfile

def create_user_profile(form_data):
    grades_raw = form_data['grades']
    grades_dict = {}
    for pair in grades_raw.split(','):
        subject, grade = pair.split(':')
        grades_dict[subject.strip()] = grade.strip()

    academic_subjects = ([s.strip() for s in form_data['academic_subjects'].split(',')] if form_data.get('academic_subjects') else [])
    interests = ([s.strip() for s in form_data['interests'].split(',')] if form_data.get('interests') else [])
    hobbies = ([s.strip() for s in form_data['hobbies'].split(',')] if form_data.get('hobbies') else [])

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

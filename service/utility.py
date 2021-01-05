def get_user_service():
    from repository.user_repository import UserRepository
    from service.user_service import UserService
    repo = UserRepository()
    return UserService(repo)


def get_student_info_service():
    from repository.student_info_repository import StudentInfoRepository
    from service.student_info_service import StudentInfoService
    repo = StudentInfoRepository()
    return StudentInfoService(repo)


def get_internship_service():
    from repository.internship_repository import InternshipRepository
    from service.internship_service import InternshipService
    repo = InternshipRepository()
    return InternshipService(repo)


def get_student_internship_service():
    from repository.student_internship_repository import StudentInternshipRepository
    from service.student_internship_serivce import StudentInternshipService
    repo = StudentInternshipRepository()
    return StudentInternshipService(repo)
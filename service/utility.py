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


def get_tutor_info_service():
    from repository.tutor_info_repository import TutorInfoRepository
    from service.tutor_info_service import TutorInfoService
    repo = TutorInfoRepository()
    return TutorInfoService(repo)


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


def get_student_activity_service():
    from repository.student_activity_repository import StudentActivityRepository
    from service.student_activity_service import StudentActivityService
    repo = StudentActivityRepository()
    return StudentActivityService(repo)


def get_declaratie_ubb_service():
    from repository.declaratie_ubb_repository import DeclaratieUBBRepository
    from service.declaratie_ubb_service import DeclaratieUBBService
    repo = DeclaratieUBBRepository()
    return DeclaratieUBBService(repo)


def get_declaratie_firma_service():
    from repository.declaratie_firma_repository import DeclaratieFirmaRepository
    from service.declaratie_firma_service import DeclaratieFirmaService
    repo = DeclaratieFirmaRepository()
    return DeclaratieFirmaService(repo)


def get_supervisor_info_service():
    from repository.supervisor_info_repository import SupervisorInfoRepository
    from service.supervisor_info_service import SupervisorInfoService
    repo = SupervisorInfoRepository()
    return SupervisorInfoService(repo)

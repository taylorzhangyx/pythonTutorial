from application.modules.user import User


def verify_identity(email, password):
    user = User.objects(email=email).first()
    if user and user.check_password(password=password):
        return True
    else:
        return False

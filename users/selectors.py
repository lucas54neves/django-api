from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_by_id(user_id: int) -> User:
    return User.objects.filter(id=user_id).first()


def list_users():
    return User.objects.all()

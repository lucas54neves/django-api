from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(*, email: str, password: str, **extra_fields) -> User:
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        **extra_fields,
    )
    return user

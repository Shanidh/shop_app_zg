from shop.models import CustomUser, UserType


def create_customer(
    username: str,
    password: str,
    email: str,
) -> None:
    user = CustomUser.objects.create_user(username=username, password=password, email=email, user_type=UserType.CUSTOMER)
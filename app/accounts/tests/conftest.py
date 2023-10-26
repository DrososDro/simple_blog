from django.contrib.auth import get_user_model
import pytest


@pytest.fixture
def create_user():
    def _create_user_factory(*, email, first_name, last_name, password):
        user = get_user_model().objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_active = True
        user.save()
        return user

    return _create_user_factory


@pytest.fixture
def create_superuser():
    user = get_user_model().objects.create_superuser(
        email="xaos@xaos.com",
        first_name="first name",
        last_name="last name",
        password="passWord",
    )
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def def_user():
    """user john doe em: John.Doe@example.com pass: test*Pass1234"""
    user_dict = {
        "first_name": "John",
        "email": "John.Doe@example.com",
        "password": "testPass1234*",
        "last_name": "Doe",
    }
    return user_dict

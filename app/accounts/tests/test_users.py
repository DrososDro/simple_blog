"""Test the user model"""
import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


pytestmark = pytest.mark.django_db


# -------------------- Test user Model--------------------
def test_create_user_with_email_should_succed(def_user) -> None:
    """Create a user and test if saved in db"""
    user = get_user_model().objects.create_user(**def_user)
    all_user = get_user_model().objects.all()
    assert len(all_user) == 1


@pytest.mark.parametrize(
    "given,expected",
    [
        ("TesT@ExaMpLe.com", "TesT@example.com"),
        ("test1@ExamPle.CoM", "test1@example.com"),
    ],
)
def test_user_normalize_email_should_succed(
    def_user,
    given,
    expected,
) -> None:
    """create user and test formalize email"""
    user = get_user_model().objects.create_user(
        first_name=def_user.get("first_name"),
        email=given,
        last_name=def_user.get("last_name"),
        password=def_user.get("password"),
    )
    assert user.email == expected


def test_user_first_last_name_lower(create_user, def_user) -> None:
    """test userl firsta and last name should be lower"""
    user = create_user(**def_user)
    assert user.first_name == def_user.get("first_name").lower()
    assert user.last_name == def_user.get("last_name").lower()
    assert user.check_password(def_user.get("password"))


def test_str_should_return_email(create_user, def_user) -> None:
    """test str methos should return mail"""
    user = create_user(**def_user)

    assert str(user) == def_user.get("email")


def test_user_create_without_mail_should_fail(create_user) -> None:
    """Creating a user without email"""
    with pytest.raises(ValueError) as e:
        create_user(
            email=None,
            first_name="first",
            last_name="last",
            password="pass",
        )

    assert str(e.value) == "Email can't be blank!"


def test_create_superuser_with_email_successfull(create_superuser):
    """
    test create_superuser function with
    email, name, surname, password,
    to return the user and save the
    model to the db
    """

    create_superuser
    user = get_user_model().objects.get(email="xaos@xaos.com")

    assert user.email == "xaos@xaos.com"
    assert user.check_password("passWord")
    assert user.is_active
    assert user.is_admin
    assert user.is_superadmin
    assert user.is_staff


def test_full_name_property_sould_succed(def_user, create_user) -> None:
    """test the property full_name of the user as title"""
    user = create_user(**def_user)
    full_name = f"{def_user['first_name']} {def_user['last_name']}".title()
    assert user.full_name == full_name


def test_has_perm_should_return_is_admin_should_succeed(
    def_user,
    create_user,
) -> None:
    """Test the has_perm method to return is admin"""
    user = create_user(**def_user)
    assert user.has_perm(user.is_admin) is False
    user.is_admin = True
    user.save()
    assert user.has_perm(user.is_admin) is True


def test_unique_of_email_should_fail(def_user, create_user) -> None:
    """Test the unique email"""
    user = create_user(**def_user)

    with pytest.raises(IntegrityError) as e:
        fail_user = create_user(**def_user)
    assert isinstance(e.value, IntegrityError)
    assert "duplicate key value violates unique constraint" in str(e.value)


def test_user_create_without_first_name_should_fail(create_user) -> None:
    """Creating a user without first"""
    with pytest.raises(ValueError) as e:
        create_user(
            email="test@test.com",
            first_name=None,
            last_name="last",
            password="pass",
        )

    assert str(e.value) == "First name can't be blank!"


def test_user_create_without_last_name_should_fail(create_user) -> None:
    """Creating a user without last_name"""
    with pytest.raises(ValueError) as e:
        create_user(
            email="test@test.com",
            first_name="first",
            last_name=None,
            password="pass",
        )

    assert str(e.value) == "Last name can't be blank!"


def test_has_module_perm_should_return_is_admin_should_succeed(
    def_user,
    create_user,
) -> None:
    """Test user if has_module_perms method to return is admin"""
    user = create_user(**def_user)
    assert user.has_module_perms(user.is_admin) is False
    user.is_admin = True
    user.save()
    assert user.has_module_perms(user.is_admin) is True

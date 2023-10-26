"""
Tests for the Django admin modifications.
"""

import pytest
from django.urls import reverse


# --------------------Test admin panel--------------------
@pytest.mark.django_db
def test_user_list(client, create_superuser, create_user, def_user):
    """
    Test that users are listed on page
    with email, first_name, last_name, is_active,created_at
    """
    url = reverse("admin:accounts_user_changelist")
    admin = create_superuser
    user = create_user(**def_user)
    client.force_login(admin)
    res = client.get(url)

    content = res.content.decode("utf-8")
    assert user.email in content
    assert user.first_name in content
    assert user.last_name in content
    assert "is_active" in content
    assert "is_admin" not in content
    assert "is_staff" not in content
    assert "is_superadmin" not in content
    assert "created_at" in content

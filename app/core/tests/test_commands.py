"""Test custom django command w8 for db"""
import pytest
from django.core.management import call_command
from unittest.mock import patch
from django.db.utils import OperationalError
from psycopg import OperationalError as Psycopg2Error


pytestmark = pytest.mark.django_db


# -------------------- Test wait for db --------------------
@patch("core.management.commands.wait_for_db.Command.check")
def test_wait_for_db_sould_connect(patched_check) -> None:
    """test if command called once"""
    patched_check.return_value = True

    call_command("wait_for_db")
    patched_check.assert_called_once_with(databases=["default"])


@patch("core.management.commands.wait_for_db.Command.check")
@patch("time.sleep")
def test_wait_for_db_delay_should_succed(patched_sleep, patched_check) -> None:
    """Test wait for db when getting errors"""
    patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

    call_command("wait_for_db")
    assert patched_check.call_count == 6
    patched_check.assert_called_with(databases=["default"])

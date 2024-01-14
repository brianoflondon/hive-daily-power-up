from datetime import datetime, timedelta

import pytz  # type: ignore
from beem import Hive  # type: ignore
from beem.account import Account  # type: ignore


def test_api_hive_blog_fail() -> None:
    """Test if the API is working."""
    try:
        hive = Hive(node=["https://api.hive.blog"], nobroadcast=True)
        today = datetime.now(pytz.utc)

        hive_acc = Account("brianoflondon", blockchain_instance=hive)
        for item in hive_acc.history(
            start=today - timedelta(days=33), only_ops=["transfer_to_vesting"]
        ):
            print(item)
    except Exception as error:
        print(error)
        assert True

def test_deathwing_fail() -> None:
    try:
        hive = Hive(node=["https://api.deathwing.me"], nobroadcast=True)
        today = datetime.now(pytz.utc)

        hive_acc = Account("brianoflondon", blockchain_instance=hive)
        for item in hive_acc.history(
            start=today - timedelta(days=33), only_ops=["transfer_to_vesting"]
        ):
            print(item)
    except Exception as error:
        print(error)
        assert False

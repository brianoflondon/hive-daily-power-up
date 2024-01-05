import logging
import os
from datetime import datetime, timedelta
from time import sleep

import pytz  # type: ignore
from beem import Hive  # type: ignore
from beem.account import Account  # type: ignore
from dotenv import load_dotenv
from single_source import get_version

__version__ = get_version(__name__, "", default_return="0.0.1")

load_dotenv()

POWERUP_ACCOUNTS = os.getenv("POWERUP_ACCOUNTS", "").split(",")
POWERUP_ACTIVE_KEYS = os.getenv("POWERUP_ACTIVE_KEYS", "").split(",")
POWERUP_AMOUNTS = os.getenv("POWERUP_AMOUNTS", "").split(",")


def power_up_month() -> None:
    """Check for last power up and power up if it is a new day."""

    for powerup_account in POWERUP_ACCOUNTS:
        powerup_active_key = POWERUP_ACTIVE_KEYS[
            POWERUP_ACCOUNTS.index(powerup_account)
        ]
        powerup_amount = POWERUP_AMOUNTS[POWERUP_ACCOUNTS.index(powerup_account)]
        logging.info(f"Checking {powerup_account} to power up {powerup_amount}HP")
        hive = Hive(
            account=powerup_account, keys=[powerup_active_key], nobroadcast=False
        )
        hive_acc = Account(powerup_account, blockchain_instance=hive)

        today = datetime.now(pytz.utc)

        power_up_days = []
        for item in hive_acc.history(
            start=today - timedelta(days=33), only_ops=["transfer_to_vesting"]
        ):
            last_powerup = datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S")
            logging.debug(f"{last_powerup=}")
            if today.month == last_powerup.month:
                power_up_days.append(last_powerup.day)

        logging.info(f"{power_up_days=}")
        if today.day not in power_up_days:
            try:
                logging.info("need to power up")
                hive_acc = Account(powerup_account, blockchain_instance=hive)
                trx = hive_acc.transfer_to_vesting(amount=powerup_amount)
                logging.info(trx["trx_id"])
            except Exception as error:
                logging.error(error)
        else:
            logging.info("no need to power up")


def main():
    print(f"Power Up Daily Version: {__version__}")
    if not POWERUP_ACCOUNTS:
        logging.error("POWERUP_ACCOUNT not set")
        return
    try:
        while True:
            logging.info("Starting main loop")
            power_up_month()
            logging.info("Sleeping for 8 hours")
            sleep(8 * 60 * 60)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt")
        exit()
    except Exception as error:
        logging.error(error)
        exit()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(module)-14s %(lineno) 5d : %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    main()

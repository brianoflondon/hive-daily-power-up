import logging
import os
from datetime import datetime, timedelta
from time import sleep

from beem import Hive  # type: ignore
from beem.account import Account  # type: ignore
from dotenv import load_dotenv
from single_source import get_version

__version__ = get_version(__name__, "", default_return="0.0.1")

load_dotenv()

POWERUP_ACCOUNT = os.getenv("POWERUP_ACCOUNT")
POWERUP_POSTING_KEY = os.getenv("POWERUP_POSTING_KEY")
POWERUP_ACTIVE_KEY = os.getenv("POWERUP_ACTIVE_KEY")
POWERUP_AMOUNT = os.getenv("POWERUP_AMOUNT")


def power_up_month():
    """Check for last power up and power up if it is a new day."""
    hive = Hive(account=POWERUP_ACCOUNT, keys=[POWERUP_ACTIVE_KEY], nobroadcast=False)
    hive_acc = Account(POWERUP_ACCOUNT, blockchain_instance=hive)
    today = datetime.utcnow()

    power_up_days = []
    for item in hive_acc.history(
        start=today - timedelta(days=33), only_ops=["transfer_to_vesting"]
    ):
        last_powerup = datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S")
        logging.info(f"{last_powerup=}")
        if today.month == last_powerup.month:
            power_up_days.append(last_powerup.day)

    logging.info(f"{power_up_days=}")
    if today.day not in power_up_days:
        logging.info("need to power up")

        hive_acc = Account(POWERUP_ACCOUNT, blockchain_instance=hive)
        trx = hive_acc.transfer_to_vesting(amount=POWERUP_AMOUNT)
        logging.info(trx["trx_id"])
        return trx["trx_id"]
    logging.info("no need to power up")


def main():
    print(f"Power Up Daily Version: {__version__}")
    if not POWERUP_ACCOUNT:
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

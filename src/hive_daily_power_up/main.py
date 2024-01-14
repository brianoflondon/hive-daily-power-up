import logging
import os
from datetime import datetime, timedelta
from time import sleep

import colorlog
import pytz  # type: ignore
from beem import Hive  # type: ignore
from beem.account import Account  # type: ignore
from dotenv import load_dotenv
from single_source import get_version
from termcolor import colored

__version__ = get_version(__name__, "", default_return="0.0.1")

load_dotenv()

POWERUP_ACCOUNTS = os.getenv("POWERUP_ACCOUNTS", "").split(",")
POWERUP_ACTIVE_KEYS = os.getenv("POWERUP_ACTIVE_KEYS", "").split(",")
POWERUP_AMOUNTS = os.getenv("POWERUP_AMOUNTS", "").split(",")

nodes = [
    "https://api.hive.blog",
    "https://api.deathwing.me",
    "https://api.hivekings.com",
    "https://anyx.io",
    "https://api.openhive.network",
]

bad_nodes = []


def power_up_month() -> None:
    """Check for last power up and power up if it is a new day."""
    success = False
    while not success:
        try:
            for powerup_account in POWERUP_ACCOUNTS:
                powerup_active_key = POWERUP_ACTIVE_KEYS[
                    POWERUP_ACCOUNTS.index(powerup_account)
                ]
                powerup_amount = POWERUP_AMOUNTS[
                    POWERUP_ACCOUNTS.index(powerup_account)
                ]
                message = colored(f"{powerup_account}", "white", attrs=["bold"])
                logging.info(f"Checking {message} to power up {powerup_amount}HP")
                hive = Hive(
                    node=[node for node in nodes if node not in bad_nodes],
                    account=powerup_account,
                    keys=[powerup_active_key],
                    nobroadcast=False,
                )
                hive_acc = Account(powerup_account, blockchain_instance=hive)

                today = datetime.now(pytz.utc)

                power_up_days = []

                for item in hive_acc.history(
                    start=today - timedelta(days=33), only_ops=["transfer_to_vesting"]
                ):
                    last_powerup = datetime.strptime(
                        item["timestamp"], "%Y-%m-%dT%H:%M:%S"
                    )
                    logging.debug(f"{last_powerup=}")
                    if today.month == last_powerup.month:
                        power_up_days.append(last_powerup.day)

                logging.info(f"{power_up_days=}")
                if today.day not in power_up_days:
                    try:
                        logging.info(
                            colored("need to power up", "white", attrs=["bold"])
                        )
                        hive_acc = Account(powerup_account, blockchain_instance=hive)
                        trx = hive_acc.transfer_to_vesting(amount=powerup_amount)
                        logging.info(trx["trx_id"])
                    except Exception as error:
                        logging.error(error)
                else:
                    logging.info("no need to power up")
                success = True
        except Exception as error:
            bad_nodes.append(hive.rpc.url)
            logging.error(f"Bad node: {hive.rpc.url}")
            logging.error(error)


def main():
    logging.info(f"Power Up Daily Version: {__version__}")
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
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)-8s %(module)-8s %(lineno) 4d : %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "blue",  # change this to the color you want
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )

    logger = colorlog.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    main()

import asyncio
import logging
import traceback
from typing import Any

import requests

from app.settings import AppSettings, get_app_settings
from app.utils.logger import setup_logging
from app.utils.utils import generate_complex_nickname, generate_password

logger = logging.getLogger(__name__)

__APP_SETTINGS: AppSettings = get_app_settings()


def create_user_obj(name: str, password: str) -> dict[str, Any]:
    return {
        "email": f"{name}@{__APP_SETTINGS.domain}",
        "raw_password": password,
        "comment": __APP_SETTINGS.user_comment,
        "quota_bytes": 10_000_000,  # 10 MB
        "global_admin": False,  # No admin
        "enabled": True,  # Account is enabled
        "change_pw_next_login": False,  # Dont need change password after login
        "enable_imap": True,
        "enable_pop": True,
        "allow_spoofing": False,
        "forward_enabled": False,
        "forward_destination": [],
        "forward_keep": True,
        "reply_enabled": False,
        "reply_startdate": "1900-01-01",
        "reply_enddate": "2999-12-31",
        "displayed_name": "",
        "spam_enabled": True,
        "spam_mark_as_read": True,
        "spam_threshold": 80,
    }


def create_user(user_obj: dict[str, Any]) -> bool:
    try:
        headers = {
            "Authorization": f"Bearer {__APP_SETTINGS.api_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            __APP_SETTINGS.api_endpoint_user_create, json=user_obj, headers=headers
        )
        response.raise_for_status()
        return True
    except requests.RequestException as ex:
        logger.exception(f"Error during POST request: {ex}")
        return False


async def create_users() -> None:
    for acc_num in range(
        __APP_SETTINGS.start_num,
        __APP_SETTINGS.accounts_count + __APP_SETTINGS.start_num,
    ):
        name = generate_complex_nickname()
        password = generate_password()
        user_obj = create_user_obj(name, password)
        if create_user(user_obj):
            title_format = __APP_SETTINGS.title_format.format(
                acc_num, __APP_SETTINGS.title_name
            )
            message = f"{title_format}\n{name}@{__APP_SETTINGS.domain}\n{password}"
            logger.info(f"User: {acc_num} was created successfully")
            with open("user_accs.txt", "a", encoding="utf-8") as file:
                file.write(f"{message}\n\n")
        else:
            logger.info(f"User: {acc_num} was not created")


async def main() -> None:
    await create_users()


if __name__ == "__main__":
    setup_logging(logger)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program terminated")
    except:  # noqa: E722
        logger.exception("An unexpected error uccurred:")
        traceback.print_exc()

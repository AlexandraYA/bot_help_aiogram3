from . import (
    support,
    support_call,
    help,
    start,
    echo
)
from aiogram import Router


def register_routers(rt: Router):
    start.router(rt)
    support.router(rt)
    support_call.router(rt)
    help.router(rt)
    echo.router(rt)

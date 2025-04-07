from . import (
    help,
    start,
    support
)
from aiogram import Router


def register_routers(rt: Router):
    start.router(rt)
    support.router(rt)
    help.router(rt)

import logging
from aiogram.exceptions import (TelegramUnauthorizedError, TelegramAPIError,
                                      DetailedAiogramError, TelegramNotFound,
                                      TelegramRetryAfter,
                                      TelegramEntityTooLarge, TelegramBadRequest)


from loader import dp

@router.error()
async def errors_handler(event: ErrorEvent):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(event.exception, DetailedAiogramError):
        logging.debug('Message is not modified, or empty')
        return True
    if isinstance(event.exception, TelegramBadRequest):
        logging.debug('Message cant be deleted')
        return True

    if isinstance(event.exception, TelegramNotFound):
        logging.debug('Message to delete not found')
        return True

    if isinstance(event.exception, TelegramUnauthorizedError):
        logging.info(f'TelegramUnauthorizedError: {event.exception}')
        return True

    if isinstance(event.exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {event.exception} \nUpdate: {update}')
        return True
    if isinstance(event.exception, TelegramRetryAfter):
        logging.exception(f'TelegramRetryAfter: {event.exception} \nUpdate: {update}')
        return True
    if isinstance(event.exception, TelegramEntityTooLarge):
        logging.exception(f'TelegramEntityTooLarge: {event.exception} \nUpdate: {update}')
        return True
    
    logging.exception(f'Update: {update} \n{event.exception}')

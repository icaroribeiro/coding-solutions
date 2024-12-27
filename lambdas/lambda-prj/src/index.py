import logging

from aws_lambda_typing import context as context_
from aws_lambda_typing import events

from config.config import Config
from prj_handler import PrjHandler

logger = logging.getLogger()


def lambda_handler(event: events.SQSEvent, context: context_.Context) -> None:
    try:
        config = Config()
        prj_handler = PrjHandler(config)
        prj_handler.do_something(event)
    except Exception:
        raise

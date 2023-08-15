import logging
from contextvars import ContextVar
from typing import Any

from pythonjsonlogger import jsonlogger


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    'Class that adds log fields required for stackdriver to display messages correctly'

    def process_log_record(self, log_record):
        log_record['severity'] = log_record['levelname']
        del log_record['levelname']
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


class Logger:
    'Class that provides a wrapper around logging. It adds standard fields to each log line'

    def __init__(self, logger: logging.Logger):
        self._logger: logging.Logger = logger
        self.context = ContextVar("messageInfo")
        self._default_context_values = {'project': 'mloh-sandbox'}
        self.context.set(self._default_context_values)

    def info(self, msg: Any, extra: dict = None, **kwargs):
        self._logger.info(msg, extra=self._add_log_fields(self.context, extra), **kwargs)

    def error(self, msg: Any, extra: dict = None, **kwargs):
        self._logger.error(msg, extra=self._add_log_fields(self.context, extra), **kwargs)

    def warning(self, msg: Any, extra: dict = None, **kwargs):
        self._logger.warning(msg, extra=self._add_log_fields(self.context, extra), **kwargs)

    def debug(self, msg: Any, extra: dict = None, **kwargs):
        self._logger.debug(msg, extra=self._add_log_fields(self.context, extra), **kwargs)

    @staticmethod
    def _add_log_fields(ctx: ContextVar, extra_fields: dict) -> dict:
        required_fields = ctx.get()
        if extra_fields is not None:
            required_fields = {**required_fields, **extra_fields}
        return required_fields

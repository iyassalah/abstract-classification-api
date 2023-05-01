# import logging
# from pprint import pformat

# from loguru import logger
# from loguru import BoundLogger
# from loguru._defaults import LOGURU_FORMAT
# from fastapi import APIRouter


# from app.logging_serivce import format_record

# router = APIRouter()


# class InterceptHandler(logging.Handler):
#     """
#     Default handler from examples in loguru documentaion.
#     """

#     def emit(self, record):
#         # Get corresponding Loguru level if it exists
#         try:
#             level = logger.level(record.levelname).name
#         except ValueError:
#             level = record.levelno

#         # Find caller from where originated the logged message
#         frame, depth = logging.currentframe(), 2
#         while frame.f_code.co_filename == logging.__file__:
#             frame = frame.f_back
#             depth += 1

#         logger.opt(depth=depth, exception=record.exc_info).log(
#             level, format_record(record)
#         )


# class LoggerService:
#     """_summary_
#         class for logging service
#     """
#     def __init__(self, log_level: str = "INFO"):
#         self.log_level = log_level
#         self.configure_logger()

#     def configure_logger(self):
#         """for configure the logger"""
#         logger.remove()
#         logger.add(
#             InterceptHandler(),
#             format=format_record,
#             level=self.log_level,
#             enqueue=True,
#         )
#     def get_logger(self, log_level: str = None) -> "Logger":
#         """
#         Get a logger instance with the specified log level.

#         Args:
#             log_level (str, optional): The log level to use for the logger. If not
#                 specified, the default log level for the logger will be used.

#         Returns:
#             Logger: A logger instance with the specified log level.
#         """
#         if log_level is None:
#             log_level = self.log_level

#         return logger.bind().opt(depth=1, lazy=True)



#     def format_record(self, record: dict) -> str:
#         """
#         Custom format for loguru loggers.
#         Uses pformat for log any data like request/response body during debug.
#         Works with logging if loguru handler it.

#         Example:
#         >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, 
#                    {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
#         >>> logger.bind(payload=).debug("users payload")
#         >>> [   {   'count': 2,
#         >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
#         >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
#         """
#         format_string = LOGURU_FORMAT

#         if record["extra"].get("payload") is not None:
#             record["extra"]["payload"] = pformat(
#                 record["extra"]["payload"], indent=4, compact=True, width=88
#             )
#             format_string += "\n<level>{extra[payload]}</level>"

#         format_string += "{exception}\n"
#         return format_string

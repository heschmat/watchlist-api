import logging

class SafeFormatter(logging.Formatter):
    """
    Ensures missing fields in format string are filled with a placeholder.
    """
    def format(self, record):
        if not hasattr(record, "email"):
            record.email = "-"
        return super().format(record)

# def get_logger(name):
#     logger = logging.getLogger(name)
#     for handler in logger.handlers:
#         for formatter in [handler.formatter]:
#             if not isinstance(formatter, SafeFormatter):
#                 handler.setFormatter(SafeFormatter(fmt=formatter._fmt, datefmt=formatter.datefmt))
#     return logger

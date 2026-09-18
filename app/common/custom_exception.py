import sys
from typing import Optional, Any


class CustomException(Exception):
    """
    Custom Exception class to capture detailed error context including
    file name, line number, original exception details, and user message.
    """

    def __init__(self, message: str, error_detail: Optional[Any] = None):
        """
        Initializes CustomException.

        Args:
            message (str): High-level error message or context description.
            error_detail (Optional[Any]): The caught exception object or traceback info.
        """
        super().__init__(message)
        self.message = message
        self.error_detail = error_detail
        self.error_message = self.get_detailed_error_message(message, error_detail)

    @staticmethod
    def get_detailed_error_message(message: str, error_detail: Optional[Any] = None) -> str:
        """
        Extracts traceback details (filename, line number, cause) to format a complete error string.
        """
        _, _, exc_tb = sys.exc_info()

        # Fallback to error_detail traceback if sys.exc_info() is empty
        if exc_tb is None and isinstance(error_detail, Exception) and error_detail.__traceback__:
            exc_tb = error_detail.__traceback__

        if exc_tb is not None:
            # Navigate to the innermost frame of the traceback
            tb = exc_tb
            while tb.tb_next is not None:
                tb = tb.tb_next
            file_name = tb.tb_frame.f_code.co_filename
            line_number = tb.tb_lineno
            cause = f" | Cause: {type(error_detail).__name__}: {error_detail}" if error_detail else ""
            return f"Error in [{file_name}] line [{line_number}] - {message}{cause}"
        elif error_detail:
            return f"{message} | Cause: {str(error_detail)}"
        else:
            return message

    def __str__(self) -> str:
        return self.error_message
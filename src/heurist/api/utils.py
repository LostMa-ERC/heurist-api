from datetime import datetime

from .constants import MAX_RETRY


def log_attempt_number(retry_state) -> None:
    """Simple logger for tenacity retry.

    Args:
        retry_state (tenacity.RetryCallState): Retry result from tenacity.
    """

    # Get the attempt number from the RetryCallState
    attempt_number = retry_state.attempt_number

    # Compose the console message
    time = datetime.now().strftime("%H:%M:%S")
    message = (
        f"[{time}] ReadTimeout error when receiving data from the Heurist API. "
        f"Retrying {attempt_number} / {MAX_RETRY} times..."
    )

    # Print the error message
    print(message)

import time
from utils import send_lex_message


def test_response_time_under_threshold():
    start = time.time()

    response = send_lex_message("Check my internet")

    end = time.time()
    duration = end - start

    assert duration < 3  # seconds
    assert "sessionState" in response

import boto3
import uuid
import time
from config import *

lex_client = boto3.client("lexv2-runtime")
lambda_client = boto3.client("lambda")
logs_client = boto3.client("logs")

def generate_session_id():
    return str(uuid.uuid4())


def send_lex_message(text, session_id=None):
    if not session_id:
        session_id = generate_session_id()

    response = lex_client.recognize_text(
        botId=LEX_BOT_ID,
        botAliasId=LEX_BOT_ALIAS_ID,
        localeId=LOCALE_ID,
        sessionId=session_id,
        text=text
    )
    return response


def invoke_lambda(payload):
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=bytes(payload, "utf-8")
    )
    return response


def get_recent_logs(filter_pattern=None, lookback_seconds=LOG_LOOKBACK_SECONDS):
    """
    Fetch recent log events from CloudWatch
    """
    end_time = int(time.time() * 1000)
    start_time = end_time - (lookback_seconds * 1000)

    kwargs = {
        "logGroupName": CLOUDWATCH_LOG_GROUP,
        "startTime": start_time,
        "endTime": end_time,
    }

    if filter_pattern:
        kwargs["filterPattern"] = filter_pattern

    response = logs_client.filter_log_events(**kwargs)

    events = response.get("events", [])
    return [event["message"] for event in events]


def wait_for_log(pattern, timeout=10):
    """
    Poll CloudWatch until a log pattern appears
    """
    start = time.time()

    while time.time() - start < timeout:
        logs = get_recent_logs()
        for log in logs:
            if pattern in log:
                return True
        time.sleep(1)

    return False

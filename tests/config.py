import os

LEX_BOT_ID = os.getenv("LEX_BOT_ID")
LEX_BOT_ALIAS_ID = os.getenv("LEX_BOT_ALIAS_ID")
LOCALE_ID = "en_US"

LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME")

TEST_USER_ID = "test-user-001"

CLOUDWATCH_LOG_GROUP = "/aws/lambda/your-lambda-function-name"
LOG_LOOKBACK_SECONDS = 60

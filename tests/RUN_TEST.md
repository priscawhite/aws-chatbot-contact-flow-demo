# **Running Automated Tests**

## Overview
This guide explains how to execute the automated test suite for the Amazon Connect + Lex + Lambda solution. These tests validate:

- End-to-end conversational flows (Amazon Lex)
- Backend logic (AWS Lambda)
- Observability (CloudWatch logs)
- Agent handoff triggers

---

## Prerequisites

### 1. AWS Account Setup
Ensure the following resources are deployed:

- Amazon Lex V2 bot (published)
- Lambda function (connected to Lex)
- Amazon Connect instance (published)
- CloudWatch logging enabled

---

### 2. Install Dependencies

`pip install boto3 pytest`

---

### 3. Configure AWS Credentials
Make sure your AWS CLI is configured:

`aws configure`

or use environment variables:

`export AWS_ACCESS_KEY_ID=your_access_key`  
`export AWS_SECRET_ACCESS_KEY=your_secret_key`  
`export AWS_DEFAULT_REGION=us-east-1`

---

### 4. Set Required Environment variables

`export LEX_BOT_ID=your_lex_bot_id`  
`export LEX_BOT_ALIAS_ID=your_lex_alias_id`  
`export LAMBDA_FUNCTION_NAME=your_lambda_function_name`  
`export CLOUDWATCH_LOG_GROUP=/aws/lambda/your-lambda-function-name`

---

## Running All Tests
From the root directory:

`pytest tests/`

---

## Running Specific Test Files

### Lex Flow Tests

`pytest tests/test_lex_flows.py`

### Lambda Tests

`pytest tests/test_lambda_flows.py`

### Fallback & Agent Hand-off

`pytest tests/test_fallback_and_handoff.py`

### CloudWatch Log Validation

`pytest tests/test_cloudwatch_logs.py`

### Performance Tests

`pytest tests/test_performance.py`

### Running with Verbose Output

`pytest -v`

## Example Test Run Output

`============================= test session starts =============================`  
`collected 10 items`
  
`test_lex_flows.py ......`  
`test_lambda_flows.py ..`  
`test_fallback_and_handoff.py ..`  
`test_cloudwatch_logs.py ..`  
`test_performance.py .`  

`============================== 10 passed in 5.12s ==============================`

## Success Criteria
All tests should pass with:
 - No assertion failures
 - Expected intents triggered
 - Lambda responses validated
 - CloudWatch logs detected
 - Response times within thresholds

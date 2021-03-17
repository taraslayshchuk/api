# API
See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.  
The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications.  
To use the SAM CLI, you need the following tools:
* [Docker](https://www.docker.com/products/docker-desktop)
* [Python 3 installed](https://www.python.org/downloads/)
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

## Run locally:

```bash
# start DynamoDB
docker-compose up
# start API Gateway
sam local start-api
```
❗️**Note**: after first run or in case of dynamodb container recreation you should:
* Upload test data to DynamoDB
```bash
./tools/create_tables.sh

```
## Workflow test example locally:
```bash
# Creating 10 connections
for x in {1..10}; do ./tools/connect.sh; done
# Getting 5 random words and send them to all open connections
for x in {1..5}; do ./tools/roll.sh; done
# Close connection by connection_id
echo '{"requestContext": {"connectionId": "<CONNECTION_ID>"}}' > events/disconnect.json
./tools/disconnect.sh
```

## Build and deploy:
```bash
sam build && sam package && sam deploy
```
❗️**Note**: after first deployemnt or in case of stack redeployment you should:
* Upload test data to DynamoDB
```bash
./tools/fill_table.sh

```
## Workflow test example with single client:
```bash
websocat wss://4m4jx88y0k.execute-api.us-east-1.amazonaws.com/prod
{"action":"roll"}
{"word": "banana"}
{"action":"roll"}
{"word": "car"}
{"action":"roll"}
{"word": "banana"}
{"action":"roll"}
{"word": "truck"}
{"action":"roll"}
{"word": "truck"}
```
## Workflow test example with multiple clients client:
```bash
# First client
$ websocat wss://4m4jx88y0k.execute-api.us-east-1.amazonaws.com/prod
{"action":"roll"}
{"word": "truck"}
{"action":"roll"}
{"word": "car"}
{"action":"roll"}
{"word": "truck"}
{"word": "banana"}
{"word": "car"}
{"word": "banana"}
^C
```
```bash
# Second client
$ websocat wss://4m4jx88y0k.execute-api.us-east-1.amazonaws.com/prod
{"word": "truck"}
{"word": "car"}
{"word": "truck"}
{"action":"roll"}
{"word": "banana"}
{"action":"roll"}
{"word": "car"}
{"action":"roll"}
{"word": "banana"}
{"action":"roll"}
{"word": "banana"}
{"action":"roll"}
{"word": "truck"}
^C
```

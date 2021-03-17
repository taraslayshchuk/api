#!/bin/bash

WORDS_TABLE_NAME="$(jq '.Parameters.WORDS_TABLE_NAME' env.json -r)"
CONNECTIONS_TABLE_NAME="$(jq '.Parameters.CONNECTIONS_TABLE_NAME' env.json -r)"
COMMON_ARGS="--endpoint-url http://localhost:8000"


aws dynamodb create-table                                                                    \
             --table-name ${WORDS_TABLE_NAME} ${COMMON_ARGS}                                 \
             --key-schema '[{"AttributeName": "id", "KeyType": "HASH"}]'                     \
             --attribute-definitions '[{"AttributeName": "id", "AttributeType": "N"}]'       \
             --provisioned-throughput '{"ReadCapacityUnits": 10, "WriteCapacityUnits": 10}'  \
&&                                                                                           \
aws dynamodb put-item                                                                        \
             --table-name ${WORDS_TABLE_NAME} ${COMMON_ARGS}                                 \
             --item '{"id": {"N": "1"}, "word":{"S":"car"}}'                                 \
&&                                                                                           \
aws dynamodb put-item                                                                        \
             --table-name ${WORDS_TABLE_NAME} ${COMMON_ARGS}                                 \
             --item '{"id": {"N": "2"}, "word":{"S":"truck"}}'                               \
&&                                                                                           \
aws dynamodb put-item                                                                        \
             --table-name ${WORDS_TABLE_NAME} ${COMMON_ARGS}                                 \
             --item '{"id": {"N": "3"}, "word":{"S":"banana"}}'                              \
&&                                                                                           \
aws dynamodb describe-table --table-name ${WORDS_TABLE_NAME} ${COMMON_ARGS}

aws dynamodb create-table                                                                          \
             --table-name ${CONNECTIONS_TABLE_NAME} ${COMMON_ARGS}                                 \
             --key-schema '[{"AttributeName": "connectionId", "KeyType": "HASH"}]'                 \
             --attribute-definitions '[{"AttributeName": "connectionId", "AttributeType": "S"}]'   \
             --provisioned-throughput '{"ReadCapacityUnits": 10, "WriteCapacityUnits": 10}'
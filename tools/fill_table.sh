#!/bin/bash

WORDS_TABLE_NAME="$(jq '.Parameters.WORDS_TABLE_NAME' env.json -r)"


aws dynamodb put-item                                                 \
             --table-name ${WORDS_TABLE_NAME}                         \
             --item '{"id": {"N": "1"}, "word":{"S":"car"}}'          \
&&                                                                    \
aws dynamodb put-item                                                 \
             --table-name ${WORDS_TABLE_NAME}                         \
             --item '{"id": {"N": "2"}, "word":{"S":"truck"}}'        \
&&                                                                    \
aws dynamodb put-item                                                 \
             --table-name ${WORDS_TABLE_NAME}                         \
             --item '{"id": {"N": "3"}, "word":{"S":"banana"}}'       \
&&                                                                    \
aws dynamodb scan                                                     \
             --table-name ${WORDS_TABLE_NAME}                         \
             --select "COUNT"                                         \
&&                                                                    \
aws dynamodb describe-table --table-name ${WORDS_TABLE_NAME}

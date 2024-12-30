import json
import logging
from typing import Any

from aws_lambda_typing import events

from services.s3_service import S3BucketParams

logger = logging.getLogger()


class SQSEventService:
    @staticmethod
    def parse_event(event: events.SQSEvent) -> S3BucketParams | None:
        try:
            record = event["Records"][0]
            body = json.loads(record["body"])
            body_message: Any
            if body.get("Message") is not None:
                body_message = json.loads(body["Message"])
                if body_message.get("eventSource") != "aws:s3":
                    message = (
                        "eventSource key is not aws:s3: "
                        f"{body_message.get('eventSource')}"
                    )
                    logger.error(message)
                    raise Exception(message)
            else:
                message = "Body does not have expected keys"
                logger.error(message)
                raise Exception(message)

            name = body_message["s3"]["bucket"]["name"]
            key = body_message["s3"]["object"]["key"]
            s3_bucket_params = S3BucketParams(name=name, key=key)
            return s3_bucket_params
        except Exception as err:
            logger.error("SQS event parsing failed!", exc_info=err)
            raise

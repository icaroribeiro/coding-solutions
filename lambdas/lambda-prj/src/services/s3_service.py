import logging

import boto3
from botocore.response import StreamingBody
from mypy_boto3_s3 import S3Client
from pydantic import BaseModel

from config.config import Config

logger = logging.getLogger()


class S3BucketParams(BaseModel):
    name: str
    key: str


class S3Service:
    __client: S3Client

    def __init__(self, config: Config) -> None:
        self.__client = boto3.client("s3", region_name=config.get_region())

    def get_object_body(self, s3_bucket_params: S3BucketParams) -> StreamingBody:
        try:
            obj = self.__client.get_object(
                Bucket=s3_bucket_params.name, Key=s3_bucket_params.key
            )
            return obj["Body"]
        except Exception as err:
            logger.error("", exc_info=err)
            raise

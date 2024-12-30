import logging

import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource
from pydantic import BaseModel

from config.config import Config

logger = logging.getLogger()


class DynamoDBTableAttrs(BaseModel):
    my_id: str
    my_position: int


class DynamoDBService:
    __resource: DynamoDBServiceResource

    def __init__(self, config: Config) -> None:
        self.__resource = boto3.resource("dynamodb", region_name=config.get_region())

    def create_record(
        self, dynamodb_table: str, ddb_table_attrs: DynamoDBTableAttrs
    ) -> None:
        try:
            table = self.__resource.Table(dynamodb_table)
            table.put_item(Item=ddb_table_attrs.model_dump())
        except Exception as err:
            logger.error("DynamoDB table record creating failed!", exc_info=err)
            raise

    def read_record(
        self, dynamodb_table: str, ddb_table_attrs: DynamoDBTableAttrs
    ) -> dict:
        try:
            table = self.__resource.Table(dynamodb_table)
            return table.get_item(Key={"my_id": ddb_table_attrs.my_id})
        except Exception as err:
            logger.error("DynamoDB table record reading failed!", exc_info=err)
            raise

import pytest
from faker import Faker
from mypy_boto3_dynamodb import DynamoDBServiceResource


class TestDynamoDBService:
    @pytest.fixture(scope="class")
    def dynamodb_table_name(
        self, dynamodb_resource: DynamoDBServiceResource, faker: Faker
    ) -> str:
        table_name = faker.pystr(min_chars=5)
        dynamodb_resource.create_table(
            AttributeDefinition=[],
            TableName=table_name,
            KeySchema=[{"AttributeName": "my_id", "KeyType": "HASH"}],
            BillingMode="PROVISIONED",
            ProvisionedThroughput={"ReadCapacityUnita": 123, "WriteCapacityUnits": 123},
        )
        return table_name

    @pytest.fixture(scope="class")
    def ddb_table_attrs(self, faker: Faker) -> DynamoDBTableAttrs:
        my_id = faker.pystr(min_chars=5)
        my_pos = faker.pyint()
        return DynamoDBTableAttrs(my_id=my_id, my_pos=my_pos)

    @pytest.fixture(scope="class")
    def dynamodb_service(self, config: Config) -> DynamoDBService:
        return DynamoDBService(config)


class TestCreateRecord(TestDynamoDBService):
    def test_should_succeed_and_return_none_when_record_is_created(
        self,
        dynamodb_table_name: str,
        ddb_table_attrs: DynamoDBTableAttrs,
        dynamodb_resource: DynamoDBServiceResource,
        dynamodb_service: DynamoDBService,
    ) -> None:
        result = dynamodb_service.create_record(dynamodb_table_name, ddb_table_attrs)

        assert result is None
        table = dynamodb_resource.Table(dynamodb_table_name)
        response = table.get_item(Key={"my_id": ddb_table_attrs.my_id})
        pos = int(response["Item"]["pos"])
        assert ddb_table_attrs.pos == pos

    def test_should_fail_and_raise_exception_when_table_does_not_exist(
        self,
        ddb_table_attrs: DynamoDBTableAttrs,
        dynamodb_service: DynamoDBService,
        faker: Faker,
    ) -> None:
        dynamodb_table_name = faker.pystr(min_chars=5)
        message = (
            "An error occurred (ResourceNotFoundException) when calling "
            + "the PuItem operation: Requested resource not found"
        )
        err = Exception(message)

        with pytest.raises(Exception) as exc_info:
            dynamodb_service.create_record(dynamodb_table_name, ddb_table_attrs)

        assert exc_info.value.args[0] == err.args[0]


class TestReadRecord(TestDynamoDBService):
    def test_should_succeed_and_return_dict_when_record_is_read(
        self,
        dynamodb_table_name: str,
        ddb_table_attrs: DynamoDBTableAttrs,
        dynamodb_resource: DynamoDBServiceResource,
        dynamodb_service: DynamoDBService,
    ) -> None:
        table = dynamodb_resource.Table(dynamodb_table_name)
        table.put_item(
            Item=ddb_table_attrs.model_dump(),
        )

        response = dynamodb_service.read_record(dynamodb_table_name, ddb_table_attrs)

        my_id = response["Item"]["my_id"]
        assert ddb_table_attrs.my_id == my_id
        pos = int(response["Item"]["pos"])
        assert ddb_table_attrs.pos == pos

    def test_should_fail_and_raise_exception_when_table_does_not_exist(
        self,
        ddb_table_attrs: DynamoDBTableAttrs,
        dynamodb_service: DynamoDBService,
        faker: Faker,
    ) -> None:
        dynamodb_table_name = faker.pystr(min_chars=5)
        message = (
            "An error occurred (ResourceNotFoundException) when calling "
            + "the GetItem operation: Requested resource not found"
        )
        err = Exception(message)

        with pytest.raises(Exception) as exc_info:
            dynamodb_service.read_record(dynamodb_table_name, ddb_table_attrs)

        assert exc_info.value.args[0] == err.args[0]

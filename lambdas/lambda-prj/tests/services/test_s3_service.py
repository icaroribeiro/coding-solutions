import pathlib
import tempfile

import pytest
import faker import Faker
from mypy_boto3_s3 import S3Client

from config.config import Config
from services.s3_service import S3BucketParams, S3Service

class TestS3Service:
    @pytest.fixture(scope="class")
    def s3_bucket_name(self, config: Config, s3_client: S3Client, faker: Faker) -> str:
        bucket = faker.pystr(min_chars=5)
        s3_client.create_bucket(
            Bucket=bucket,
            ACL="public-read",
            CreateBucketConfiguration={"LocationConstraint": config.get_region()},
        )
        return bucket
    
    @pytest.fixture(scope="class")
    def s3_service(self, config: Config) -> S3Service:
        return S3Service(config)
    
class TestGetObjectBody(TestS3Service):
    def test_should_succeed_and_return_object_body(self, s3_bucket_name: str, s3_client: S3Client, s3_service: S3Service, faker: Faker) -> None:
        s3_bucket_key = faker.pystr(min_chars=5)
        file_content = faker.pystr(min_chars=5)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = pathlib.Path(temp_dir, f"{faker.pystr(min_chars=5)}.txt")
            temp_file_path.write_text(file_content)
            s3_client.upload_file(
                Filename=temp_file_path, Bucket=s3_bucket_name, Key=s3_bucket_key
            )
        s3_bucket_params = S3BucketParams(name=s3_bucket_name, key=s3_bucket_key)

        result = s3_service.get_object_body(s3_bucket_params)

        assert result.read() == file_content.encode()

    def test_should_fail_and_raise_exception_when_s3_bucket_key_does_not_exist(self, s3_bucket_name: str, s3_service: S3Service, faker: Faker) -> None:
        s3_bucket_key = faker.pystr(min_chars=5)
        s3_bucket_params = S3BucketParams(name=s3_bucket_name, key=s3_bucket_key)
        message = (
            "An error occurred (NoSuchKey) when calling the GetObject operation: "
            + "The specified key does not exist."
        )
        err = Exception(message)

        with pytest.raises(Exception) as exc_info:
            s3_service.get_object_body(s3_bucket_params)

        assert exc_info.value.args[0] == err.args
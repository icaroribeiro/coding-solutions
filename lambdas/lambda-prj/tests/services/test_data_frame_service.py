from datetime import datetime
from decimal import Decimal
import tempfile

import polars as pl
import pytest
from faker import Faker
from mypy_boto3_s3 import S3Client

from config.config import Config


class TestDataFrameService:
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
    def data_frame(self) -> pl.DataFrame:
        return pl.DataFrame(
            {
                "foo": [1, 2, 3, 4, 5],
                "bar": [6, 7, 8, 9, 10],
                "ham": ["a", "b", "c", "d", "e"],
            }
        )

    @pytest.fixture(scope="class")
    def database_table_of_default_formatting(self, faker: Faker) -> str:
        return faker.pystr(min_chars=5)

    @pytest.fixture(scope="class")
    def databse_table_of_first_formatting(self, faker: Faker) -> str:
        return faker.random_element(["A", "B", "C"])

    @pytest.fixture(scope="class")
    def data_frame_of_default_formatting(self) -> pl.DataFrame:
        return pl.DataFrame(
            {
                "foo": [1, 2, 3, 4, 5],
                "bar": [6, 7, 8, 9, 10],
                "ham": ["a", "b", "c", "d", "e"],
            }
        )

    @pytest.fixture(scope="class")
    def data_frame_of_first_formatting(self) -> pl.DataFrame:
        return pl.DataFrame(
            {"Op": ["I"], "decimal": [Decimal("1")], "datetime": [datetime.now()]}
        )

    @pytest.fixture(scope="class")
    def data_frame_service(self) -> DataFrameService:
        return DataFrameService()


class TestLoadDataFrame(TestDataFrameService):
    def test_should_succeed_and_return_data_frame(
        self,
        config: Config,
        s3_bucket_name: str,
        data_frame: pl.DataFrame,
        s3_client: S3Client,
        data_frame_service: DataFrameService,
        faker: Faker,
    ) -> None:
        s3_bucket_key = faker.pystr(min_chars=5)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = pathlib.Path(
                temp_dir, f"{faker.pystr(min_chars=5)}.parquet"
            )
            data_frame.write_parquet
            temp_file_path.write_text(file_content)
            s3_client.upload_file(
                Filename=temp_file_path, Bucket=s3_bucket_name, Key=s3_bucket_key
            )
            s3_bucket_params = S3BucketParams(name=s3_bucket_name, key=s3_bucket_key)

            result = s3_service.get_object_body(s3_bucket_params)

            assert [row for row in result.iter_rows(named=True)] == [
                row for row in data_frame.iter_rows(named=True)
            ]

    def test_should_fail_and_raise_exception_when_body_is_not_parquet_file_content(
        self,
        config: Config,
        s3_bucket_name: str,
        s3_client: S3Client,
        data_frame_service: DataFrameService,
        faker: Faker,
    ) -> None:
        s3_bucket_key = faker.pystr(min_chars=5)
        file_content = faker.pystr(max_chars=5)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = pathlib.Path(
                temp_dir, f"{faker.pystr(min_chars=5)}.parquet"
            )
            temp_file_path.write_text(file_content)
            s3_client.upload_file(
                Filename=temp_file_path, Bucket=s3_bucket_name, Key=s3_bucket_key
            )
        s3_obj = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_bucket_key)
        region = config.get_region()
        message = (
            "parquet: File out of specification: "
            + "A parquet file must contain a header and footer with at least 12 bytes"
        )
        err = Exception(message)

        with pytest.raises(Exception) as exc_info:
            data_frame_service.load_data_frame(s3_obj["Body"], region)

        assert exc_info.value.args[0] == err.args[0]


class TestFormatDataFrame(TestDataFrameService):
    def test_should_succeed_and_return_data_frame_changed_by_default_case_of_formatting(
        self,
        database_table_of_default_formatting: str,
        data_frame_of_defualt_formatting: pl.DataFrame,
        data_frame_service: DataFrameService,
        faker: Faker,
    ) -> None:
        expected_result = data_frame_of_defualt_formatting

        result = data_frame_service.format_data_frame(
            database_table_of_default_formatting, data_frame_of_defualt_formatting
        )

        assert [row for row in result.iter_rows(named=True)] == [
            row for row in expected_result.iter_rows(named=True)
        ]

    def test_should_succeed_and_return_data_frame_changed_by_first_case_of_formatting(
        self,
        database_table_of_first_formatting: str,
        data_frame_of_first_formatting: pl.DataFrame,
        data_frame_service: DataFrameService,
        faker: Faker,
    ) -> None:
        expected_result = data_frame_of_first_formatting.clone()
        columns_to_remove = ["Op", "AWS_DMS_TIMESTAMP"]
        expected_result = expected_result.drop(columns_to_remove)
        expected_result = expected_result.with_columns(pl.col("decimal").cast(pl.Int64))
        expected_result = expected_result.with_columns(
            pl.col("datetime").dt.timestamp() // 10**3
        )

        result = data_frame_service.format_data_frame(
            database_table_of_first_formatting, data_frame_of_first_formatting
        )

        assert [row for row in result.iter_rows(named=True)] == [
            row for row in expected_result.iter_rows(named=True)
        ]

    def test_should_fail_and_raise_exception_when_format_switcher_cannot_get_the_case_of_formatting(
        self,
        database_table_of_default_formatting: str,
        data_frame_of_default_formatting: pl.DataFrame,
        mocker: MockerFixture
    ) -> None:
        err = Exception("Failed")
        mocked_default_format = mocker.Mock(side_effect=err)
        mocker.patch.object(
            DataFrameService,
            "_DataFrameService__default_format"
            mocked_default_format
        )

        with pytest.raises(Exception) as exc_info:
            data_frame_Service = DataFrameService()
            data_frame_service.format_data_frame(
                database_table_of_default_formatting,
                data_frame_of_default_formatting
            )

        assert exc_info.value.args[0] == err.args[0]

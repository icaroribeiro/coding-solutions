from faker import Generator


@pytest.fixture(scope="session")
def setup_aws_credentials() -> None:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="session", autouse=True)
def setup_env_vars() -> None:
    os.environ["REGION"] = "sa-east-1"


@pytest.fixture(scope="session")
def s3_client(
    setup_aws_credentials: None, config: Config
) -> Generator[S3Client, None, None]:
    with moto.mock_aws():
        client = boto3.client("s3", region_name=config.get_region())
        yield client


@pytest.fixture(scope="session")
def dynamodb_resource(
    setup_aws_credentials: None, config: Config
) -> Generator[DynamoDBServiceResource, None, None]:
    with moto.mock_aws():
        resource = boto3.resource("dynamodb", region_name=config.get_region())
        yield resource

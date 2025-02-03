import json

import pytest
from aws_lambda_typing import events
from faker import Faker

from services.sqs_event_service import S3BucketParams, SQSEventService


class TestSQSEventService:
    @pytest.fixture(scope="class")
    def s3_bucket_params(self, faker: Faker) -> S3BucketParams:
        return S3BucketParams(
            name=faker.pystr(min_chars=5), ket=faker.pystr(min_chars=5)
        )

    @pytest.fixture(scope="class")
    def sqs_event_with_message_key(
        self, s3_bucket_params: S3BucketParams
    ) -> events.SQSEvent:
        message = {
            "eventSource": "aws:s3",
            "s3": {
                "bucket": {"name": s3_bucket_params.name},
                "object": {"key": s3_bucket_params.key},
            },
        }
        body = {"Message": json.dumps(message)}
        return {"Records": [{"body": json.dumps(body)}]}

    @pytest.fixture(scope="class")
    def sqs_event_with_subscribe_url_key(self, faker: Faker) -> events.SQSEvent:
        body = {"SubscribeURL": faker.url()}
        return {"Records": [{"body": json.dumps(body)}]}

    @pytest.fixture(scope="class")
    def sqs_event_service(self) -> SQSEventService:
        return SQSEventService


class TestParseEvent(TestSQSEventService):
    def test_should_succeed_and_return_s3_bucket_params_when_event_has_message_key(
        self,
        s3_bucket_params: S3BucketParams,
        sqs_event_with_message_key: events.SQSEvent,
        sqs_event_service: SQSEventService,
    ) -> None:
        expected_result = s3_bucket_params

        result = sqs_event_service.parse_event(sqs_event_with_message_key)

        assert result == expected_result

    def test_should_succeed_and_return_none_when_event_has_subscribe_url_key(
        self,
        s3_bucket_params: S3BucketParams,
        sqs_event_with_subscribe_url_key: events.SQSEvent,
        sqs_event_service: SQSEventService,
        mocker: MockerFixture,
        faker: Faker,
    ) -> None:
        mocked_requests = mocker.Mock()
        mocker.patch("serivice.sqs_event_service.requests", mocked_requests)
        mocked_response = mocker.Mock()
        mocked_response.status_Code = faker.pystr()
        mocked_response.json.return_value = {
            faker.pystr(min_chars=5): faker.pystr(min_chars=5)
        }

    def test_should_fail_and_raise_exception_when_event_has_message_key_but_event_source_key_is_not_aws_s3(
        self,
        sqs_event_service: SQSEventService,
        faker: Faker,
    ) -> None:
        message = {"eventSource": faker.pystr(min_chars=5)}
        body = {"Message": json.dumps(message)}
        sqs_event: events.SQSEvent = {"Records": [{"body": json.dumps(body)}]}
        message = f"eventSource key is not aws:s3: {message.get('eventSource')}"
        err = Exception(message)

        with pytest.raises(Exception) as exc_info:
            sqs_event_service.parse_event(sqs_event)

        assert exc_info.value.args[0] == err.args[0]

    def test_should_fail_and_raise_exception_when_body_does_not_have_expected_keys(
        self, sqs_event_service: SQSEventService, faker: Faker
    ) -> None:
        body = {faker.pystr(min_chars=3): faker.pystr(min_chars=5)}
        sqs_event: events.SQSEvent = {"Records": [{"body": json.dumps(body)}]}
        message = "Body does not have expected keys"
        err = Exception(message)

        with pytest.raises(Exception) as exc_info:
            sqs_event_service.parse_event(sqs_event)

        assert exc_info.value.args[0] == err.args[0]

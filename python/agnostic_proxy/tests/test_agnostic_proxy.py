import unittest
from unittest.mock import patch, MagicMock, PropertyMock, ANY

import requests

from shared.agnostic_proxy import ProxyRequest


class TestProxyRequest(unittest.TestCase):
    def test_succeeded_when_a_request_is_performed_once_again_using_retry_mechanism(self):
        test_response = self._decorated_function

        with patch("shared.agnostic_proxy.retry") as mocked_retry:
            mocked_retry.return_value = test_response

            proxy_request = ProxyRequest()
            test_return_value = proxy_request.handle_request()

            self.assertEqual(test_return_value.return_value.content, test_response().return_value.content)
            mocked_retry.assert_called_once_with(proxy_request.make_request, stop=ANY, wait=ANY)

    def test_succeeded_when_a_request_is_performed_once_again_using_retry_mechanism_with_max_attempt_number_defined(
            self):
        max_attempt_number = 5
        test_response = self._decorated_function

        with patch("shared.agnostic_proxy.retry") as mocked_retry:
            mocked_retry.return_value = test_response

            proxy_request = ProxyRequest()
            proxy_request.max_attempt_number = max_attempt_number
            test_return_value = proxy_request.handle_request()

            self.assertEqual(test_return_value.return_value.content, test_response().return_value.content)
            mocked_retry.assert_called_once_with(proxy_request.make_request, stop=ANY, wait=ANY)

    def test_failed_when_a_request_exception_is_thrown_while_trying_to_retry_a_request(self):
        with patch("shared.agnostic_proxy.retry") as mocked_retry:
            mocked_retry.side_effect = requests.RequestException("failed")
            with self.assertRaises(requests.RequestException):
                proxy_request = ProxyRequest()
                proxy_request.handle_request()

                mocked_retry.assert_called_once_with(proxy_request.make_request, stop=ANY, wait=ANY)

    def test_failed_when_a_exception_is_thrown_while_trying_to_retry_a_request(self):
        with patch("shared.agnostic_proxy.retry") as mocked_retry:
            mocked_retry.side_effect = Exception("failed")
            with self.assertRaises(Exception):
                proxy_request = ProxyRequest()
                proxy_request.handle_request()

            mocked_retry.assert_called_once_with(proxy_request.make_request, stop=ANY, wait=ANY)

    @staticmethod
    def _decorated_function(*args, **kwargs):
        mocked_response = MagicMock()
        type(mocked_response.return_value).content = PropertyMock(return_value="content")
        return mocked_response

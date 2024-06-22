import random
from typing import Any, Optional

import requests
from requests import Session
from tenacity import retry, stop_after_attempt, wait_fixed


# X-Max-Attempt-Number

class ProxyRequest:
    max_attempt_number: Optional[int] = None

    def handle_request(self):
        headers = {}
        host = "https://httpbin.org/post".encode("utf-8")
        method = "post"
        body = None

        try:
            max_attempt_number = 1
            if self.max_attempt_number:
                max_attempt_number = self.max_attempt_number

            session = requests.Session()
            retry_request = retry(self.make_request, stop=stop_after_attempt(max_attempt_number), wait=wait_fixed(5))

            response = retry_request(session, method, host, headers, body)

            print(f'SUCCESS: {response.content}')

            return response
        except requests.RequestException as e:
            print(f'FAILED: {e}')
            raise
        except Exception as e:
            print(f'FAILED: {e}')
            raise

    @staticmethod
    def make_request(session: Session, method: str, host: bytes, headers: dict, body: Any):
        return getattr(session, method)(
            host,
            headers=headers,
            data=body
        )


proxy_request = ProxyRequest()
proxy_request.handle_request()

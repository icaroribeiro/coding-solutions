import logging
import time

import requests
import zeep

from config.config import get_environment, get_guid_tenant, get_password, get_user
from work_steps.step_1.step_1 import run as run_step_1
from work_steps.step_2.step_2 import run as run_step_2
from work_steps.step_3.step_3 import run as run_step_3

logging.basicConfig(
    format="%(asctime)s: %(message)s", datefmt="%Y-%m-%d %H:%M", level=logging.INFO
)


def create_client() -> zeep.Client:
    """Create a client to perform SOAP API requests.

    :return: The interface for interacting with a SOAP server
    :rtype: int
    """
    session = requests.Session()
    session.verify = True
    transport = zeep.Transport(cache=None, session=session)
    # return zeep.Client(wsdl="http://localhost:8000/?wsdl", transport=transport)
    return zeep.Client(
        wsdl="https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php?wsdl",
        transport=transport,
    )


def create_auth_header(
    user: str, password: str, guid_tenant: str, environment: str
) -> dict[str, str]:
    """Creates an authentication header to perform SOAP API reuqests.

    :param str user: The user credential
    :param str password: The password credential
    :param str guid_tenant: The tenant GUID identifier
    :param str environment: The environment value
    :return: The authentication header
    :rtype: dict[str, str]
    """
    return {}


if __name__ == "__main__":
    logging.info("The script execution has started...")
    st = time.time()
    client = create_client()

    user = get_user()
    password = get_password()
    guid_tenant = get_guid_tenant()
    environment = get_environment()
    auth_header = create_auth_header(
        user=user, password=password, guid_tenant=guid_tenant, environment=environment
    )

    list_of_obj_1s = run_step_1(client=client, auth_header=auth_header)

    list_of_obj_2s = run_step_2(
        client=client, auth_header=auth_header, list_of_obj_1s=list_of_obj_1s
    )

    run_step_3(list_of_obj_2s=list_of_obj_2s)
    logging.info(f"Time: {(time.time() - st):.2f}")
    logging.info("The script execution has finished successfully")

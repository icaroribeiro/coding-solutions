from pydantic import BaseModel


class ServiceAccountInfoModel(BaseModel):
    private_key: str
    client_email: str
    token_uri: str

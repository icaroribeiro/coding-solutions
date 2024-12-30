from pydantic import BaseModel


class Greetings(BaseModel):
    msg: str


def say_hello() -> str:
    msg: str = "Hello, Github Actions"
    greetings = Greetings(msg=msg)
    return greetings.msg

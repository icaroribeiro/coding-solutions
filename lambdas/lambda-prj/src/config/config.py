import logging
import os

logger = logging.getLogger()


class Config:
    def get_region(self) -> str:
        return self.__get_env_var("REGION")

    @staticmethod
    def __get_env_var(name: str) -> str:
        if os.eviron.get(name) is None:
            message = f"{name} environment variable isn't set!"
            logger.error(message)
            raise Exception(message)
        return os.environ.get(name)

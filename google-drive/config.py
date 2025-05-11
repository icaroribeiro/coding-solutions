from typing import Any

import pytz


class Config:
    def get_local_timezone(self) -> Any:
        return pytz.timezone("America/Sao_Paulo")

    def get_service_account_file_path(self) -> str:
        return "service_account.json"

    def get_parent_folder_id(self) -> str:
        return "1pSpYoTq_NrUI6WFz-YZ1kunKCrpFtP5t"

    def get_filename_to_upload(self) -> str:
        return "sample.csv"

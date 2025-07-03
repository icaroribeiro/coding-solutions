import tempfile
from datetime import datetime
from typing import Dict

import pandas as pd
from config import Config

# from google_drive_util_1 import GoogleDriveUtil
from google_drive_util_2 import GoogleDriveUtil
from service_account_info_model import ServiceAccountInfoModel


def main(config: Config, reference_date: datetime) -> None:
    data_frame: pd.DataFrame
    try:
        table_data = {
            "id": [1010],
            "name": ["Icaro Ribeiro"],
            "role": ["user"],
            "zip_code": [112233],
        }
        data_frame = pd.DataFrame(data=table_data)
    except Exception as error:
        print(f"error: {error}")
        raise

    service_account_info = ServiceAccountInfoModel(
        private_key="",
        client_email="",
        token_uri="",
    ).model_dump()
    # service_account_file_path = config.get_service_account_file_path()
    # google_drive_util = GoogleDriveUtil(
    #     service_account_file_path=service_account_file_path
    # )
    google_drive_util = GoogleDriveUtil(service_account_info=service_account_info)
    filename = config.get_filename_to_upload()
    dst_filename = f"{reference_date}_{filename}"
    temp_dst_filename = f"{dst_filename.replace('.csv', '_tmp.csv')}"
    parent_folder_id = config.get_parent_folder_id()
    uploaded_file_id: str
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv"
        ) as temp_file:
            src_filename = temp_file.name
            data_frame.to_csv(path_or_buf=src_filename, index=False)
            uploaded_file_id = google_drive_util.upload_file(
                src_filename=src_filename,
                dst_filename=temp_dst_filename,
                mime_type="text/csv",
                parent_folder_id=parent_folder_id,
            )
            print(f"Uploaded temporary file with ID: {uploaded_file_id}")
    except Exception as error:
        print(f"error: {error}")
        raise

    folder_items: Dict[str, str] = dict()
    selected_item_id: str = ""
    try:
        folder_items = google_drive_util.list_folder(parent_folder_id=parent_folder_id)
        if len(folder_items) > 0:
            for item in folder_items:
                if item["name"] == dst_filename and item["mimeType"] == "text/csv":
                    selected_item_id = item["id"]
                    print(f"Selected file with ID: {selected_item_id}")
                    break
    except Exception as error:
        print(f"error: {error}")
        raise

    if len(selected_item_id) > 0:
        try:
            google_drive_util.delete_file_or_folder(file_or_folder_id=selected_item_id)
            print(f"Deleted file with ID: {selected_item_id}")
        except Exception as error:
            print(f"error: {error}")
            raise

    try:
        google_drive_util.rename_file(file_id=uploaded_file_id, new_name=dst_filename)
        print(f"Renamed temporary file with ID: {uploaded_file_id}")
    except Exception as error:
        print(f"error: {error}")
        raise


if __name__ == "__main__":
    config = Config()
    reference_date = datetime.now(tz=config.get_local_timezone()).date()
    main(config=config, reference_date=reference_date)

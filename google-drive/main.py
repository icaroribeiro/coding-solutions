import tempfile
from datetime import datetime
from typing import Dict

import pandas as pd
import pytz
from config import Config
from google_drive_utils import GoogleDriveUtils


def main(config: Config, reference_date: datetime) -> None:
    table_data = {"id": [1], "name": ["Icaro"], "role": ["admin"], "zip_code": [12345]}
    data_frame = pd.DataFrame(data=table_data)

    service_account_file_path = config.get_service_account_file_path()
    google_drive_utils = GoogleDriveUtils(
        service_account_file_path=service_account_file_path
    )
    items: Dict[str, str] = dict()
    try:
        items = google_drive_utils.list_folder(
            parent_folder_id=config.get_parent_folder_id()
        )
    except Exception as error:
        print(f"error: {error}")
        raise

    filename = "sample.csv"
    dst_filename = f"{reference_date}_{filename}"
    try:
        if len(items) > 0:
            for item in items:
                if item["name"] == dst_filename and item["mimeType"] == "text/csv":
                    deleted_file_id = item["id"]
                    google_drive_utils.delete_file_or_folder(
                        file_or_folder_id=deleted_file_id
                    )
                    print(f"Deleted file with ID: {deleted_file_id}")
                    break
    except Exception as error:
        print(f"error: {error}")
        raise

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv"
        ) as temp_file:
            src_filename = temp_file.name
            data_frame.to_csv(path_or_buf=src_filename, index=False)
            uploaded_file_id = google_drive_utils.upload_file(
                src_filename=src_filename,
                dst_filename=dst_filename,
                mime_type="text/csv",
                parent_folder_id=config.get_parent_folder_id(),
            )
            print(f"Uploaded file with ID: {uploaded_file_id}")
    except Exception as error:
        print(f"error: {error}")
        raise


if __name__ == "__main__":
    config = Config()
    reference_date = datetime.now(tz=pytz.timezone("America/Sao_Paulo")).date()
    main(config=config, reference_date=reference_date)

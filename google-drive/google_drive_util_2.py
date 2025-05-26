from typing import Any, Dict

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class GoogleDriveUtil:
    _drive_service: Any

    def __init__(self, service_account_info: Dict[str, str]) -> None:
        scopes = ["https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_info(
            info=service_account_info, scopes=scopes
        )
        self._drive_service = build("drive", "v3", credentials=credentials)

    def list_folder(self, parent_folder_id=None) -> Dict[str, str]:
        results = (
            self._drive_service.files()
            .list(
                q=f"'{parent_folder_id}' in parents and trashed=false"
                if parent_folder_id
                else None,
                pageSize=1000,
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
            )
            .execute()
        )

        return results.get("files", [])

    def upload_file(
        self,
        src_filename: str,
        dst_filename: str,
        mime_type="text/plain",
        parent_folder_id=None,
    ) -> str:
        file_metadata = {
            "name": dst_filename,
            "parents": [parent_folder_id] if parent_folder_id else [],
        }

        media = MediaFileUpload(
            filename=src_filename, mimetype=mime_type, resumable=True
        )

        result = (
            self._drive_service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            )
            .execute()
        )

        return result.get("id")

    def rename_file(self, file_id: str, new_name: str):
        file_metadata = {
            "name": new_name,
        }
        self._drive_service.files().update(fileId=file_id, body=file_metadata).execute()

    def delete_file_or_folder(self, file_or_folder_id: str) -> None:
        self._drive_service.files().delete(fileId=file_or_folder_id).execute()

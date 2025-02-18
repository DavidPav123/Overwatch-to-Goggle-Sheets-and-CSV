from os.path import exists
from typing import Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  #type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from googleapiclient.discovery import build # type: ignore

# Scopes the program is allowed to access
SCOPES: list[str] = ["https://www.googleapis.com/auth/spreadsheets"]


def update_sheet(
    values_to_update: list[list[str]], range_to_update: str, spreadsheet_id: str
) -> None:
    creds: Optional[Credentials] = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES) # type: ignore
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:  # type: ignore
            creds.refresh(Request())  # type: ignore
        else:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(  # type: ignore
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)  # type: ignore
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json()) # type: ignore

    try:
        service = build("sheets", "v4", credentials=creds) # type: ignore

        value_range_body = {"values": values_to_update}

        request = ( # type: ignore
            service.spreadsheets() # type: ignore
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_to_update,
                valueInputOption="USER_ENTERED",
                body=value_range_body,
            )
        )
        _ = request.execute() # type: ignore
    except HttpError as err:
        print(err)

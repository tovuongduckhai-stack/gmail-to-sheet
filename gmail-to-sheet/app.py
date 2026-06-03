import os, json, pickle
import gspread
from flask import Flask
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)

@app.route("/")
def home():
    return "App chạy thành công! Truy cập /update-sheet để cập nhật dữ liệu."

@app.route("/update-sheet")
def update_sheet():
    # Lấy credentials từ biến môi trường
    google_creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    sheets_creds = service_account.Credentials.from_service_account_info(
        json.loads(google_creds_json),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(sheets_creds)
    sheet = gc.open_by_key(os.environ.get("SHEET_ID")).sheet1

    # Clear sheet + header
    sheet.clear()
    sheet.append_row(["ID", "Snippet"])

    # Gmail API (OAuth token từ biến môi trường)
    token_bytes = os.environ.get("GOOGLE_TOKEN")
    creds = None
    if token_bytes:
        creds = pickle.loads(bytes(token_bytes, "utf-8"))

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    gmail_service = build("gmail", "v1", credentials=creds)

    # Fetch 10 emails
    results = gmail_service.users().messages().list(userId="me", maxResults=10).execute()
    messages = results.get("messages", [])
    for msg in messages:
        data = gmail_service.users().messages().get(userId="me", id=msg["id"]).execute()
        snippet = data.get("snippet")[:200]
        sheet.append_row([data["id"], snippet])

    return "Sheet updated!"

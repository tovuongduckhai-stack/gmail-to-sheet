import os, json
import gspread
from flask import Flask
from google.oauth2 import service_account

app = Flask(__name__)

@app.route("/")
def home():
    return "App is running! Visit /update-sheet to update the data."

@app.route("/update-sheet")
def update_sheet():
    # Lấy credentials từ biến môi trường
    google_creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    creds_info = json.loads(google_creds_json)

    # Tạo credentials cho Google Sheets
    sheets_creds = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    # Authorize gspread
    gc = gspread.authorize(sheets_creds)
    sheet = gc.open_by_key(os.environ.get("SHEET_ID")).sheet1

    # Clear sheet + header
    sheet.clear()
    sheet.append_row(["ID", "Snippet"])

    # Demo: ghi dữ liệu mẫu
    for i in range(1, 6):
        sheet.append_row([f"msg_{i}", f"This is snippet number {i}"])

    return "Sheet updated successfully!"

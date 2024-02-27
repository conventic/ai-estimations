import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME')
GCP_CREDENTIALS_FILE_PATH = os.getenv('GCP_CREDENTIALS_FILE_PATH')
client = OpenAI(api_key=OPENAI_API_KEY)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    GCP_CREDENTIALS_FILE_PATH, scope)

print(
    f"Starting to estimate user stories from sheet '{GOOGLE_SHEET_NAME}' with '{GCP_CREDENTIALS_FILE_PATH}'...")
gs_client = gspread.authorize(credentials)
sheet = gs_client.open(GOOGLE_SHEET_NAME).sheet1

COLUMN_USER_STORY = 1  # column A
COLUMN_DESCRIPTION = 2  # column B
COLUMN_ESTIMATION_RESULT = 3  # column C
STARTING_ROW = 2  # Start at 2, to skip the header row


for i in range(STARTING_ROW, sheet.row_count + 1):
    user_story = sheet.cell(i, COLUMN_USER_STORY).value
    description = sheet.cell(i, COLUMN_DESCRIPTION).value

    if not user_story and not description:
        break  # End when we reach an empty row

    context = f"User Story: \n```\n{user_story}\n```\n Description: \n```\n{description}\n```"

    messages = [
        {"role": "system",
            "content": "Enter the estimated duration in person-days, how much time a software engineering team will need for implementation (rough estimate)."},
        {"role": "user", "content": f"{context}\nEstimated duration in person-days as a number:"}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    print(context)
    estimated_duration = response.choices[0].message.content.strip()
    print(f"Estimation result: {estimated_duration}")
    sheet.update_cell(i, COLUMN_ESTIMATION_RESULT, estimated_duration)

print("Done! The estimated durations have been inserted into the Google Sheet.")

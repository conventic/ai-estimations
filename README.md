# AI Estimations

1. Enabled `Google Drive API` and `Google Sheets API`
2. GCP **service account** to download credentials.json
3. Make sure your google sheet is shared with the service account
4. Generate separate API key for OpenAI: https://platform.openai.com/api-keys
5. Run `make setup` to create valid `.env` file and to install dependencies
6. Run `make run` to generate estimations in google sheet

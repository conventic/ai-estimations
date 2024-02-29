DEBUG ?= 0

ifeq ($(DEBUG),0)
.SILENT:
endif

.PHONY: run
run: venv .env
	. venv/bin/activate
	python main.py

.env:
	echo "Setting up .env file..."
	read -p "Enter your OPENAI_API_KEY: " openai_api_key
	read -p "Enter GCP_CREDENTIALS_FILE_PATH [./credentials.json]: " gcp_credentials_file_path
	read -p "Enter GOOGLE_SHEET_NAME [user_stories_spreadsheet]: " google_sheet_name
	gcp_credentials_file_path=$${gcp_credentials_file_path:-./credentials.json}
	google_sheet_name=$${google_sheet_name:-user_stories_spreadsheet}
	client_email=$$(grep '"client_email":' "$$gcp_credentials_file_path" | sed -E 's/.*"client_email": "([^"]+)",.*/\1/')
	echo "Make sure your google sheet \"$$google_sheet_name\" is shared with the service account $$client_email."
	read -p "Press enter to confirm you have shared your Google Sheet \"$$google_sheet_name\" with the service account email $$client_email: " confirm
	echo "OPENAI_API_KEY=$$openai_api_key" > .env
	echo "GCP_CREDENTIALS_FILE_PATH=$$gcp_credentials_file_path" >> .env
	echo "GOOGLE_SHEET_NAME=$$google_sheet_name" >> .env
	echo ".env file created successfully."

venv:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

.PHONY: setup_new
setup_new: del_env .env

.PHONY: del_env
	rm .env

.ONESHELL:
.SHELLFLAGS = -euc

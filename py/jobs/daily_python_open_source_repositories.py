"""This script is used to get the daily python open source repositories from the Gemini API and send it to the email.

Needs the following environment variables:
- GEMINI_API_KEY
- RESEND_API_KEY
- EMAIL
- GCP_BUCKET_NAME
"""

from py.llm_request.request_gemini import request_gemini, GeminiModels
from py.send_email import send_email
from py.prompts.daily_python_open_source_repositories import daily_python_open_source_repositories_prompt
from py.use_gcp_storage import get_gcs_file_as_text, upload_to_gcs_file
import json
import yaml
import os
from datetime import datetime
from py.utils import extract_outermost_braces

PYTHON_OPEN_SOURCE_REPOSITORIES_HISTORY_FILE = "python_open_source_repositories_history.txt"

# Load config from environment variables (for GitHub Actions) or config files (for local)
def load_config():
    if os.getenv('GEMINI_API_KEY'):
        # GitHub Actions mode - use environment variables
        return {
            'gemini_api_key': os.getenv('GEMINI_API_KEY'),
            'resend_api_key': os.getenv('RESEND_API_KEY'),
            'email': os.getenv('EMAIL'),
            'bucket_name': os.getenv('GCP_BUCKET_NAME', 'productivity-jyn')
        }
    else:
        # Local mode - use config files
        with open('config/api_keys.yml', 'r') as file:
            api_keys = yaml.safe_load(file)
        
        with open('config/gcp_config.yml', 'r') as file:
            gcp_config = yaml.safe_load(file)
            
        return {
            'gemini_api_key': api_keys['gemini_api_key'],
            'resend_api_key': api_keys['resend_api_key'],
            'email': api_keys['email'],
            'bucket_name': gcp_config['bucket_name']
        }

def get_daily_python_open_source_repositories():
    config = load_config()
    
    # Set environment variables for the imported modules
    os.environ['GEMINI_API_KEY'] = config['gemini_api_key']
    os.environ['RESEND_API_KEY'] = config['resend_api_key']
    os.environ['EMAIL'] = config['email']
    os.environ['GCP_BUCKET_NAME'] = config['bucket_name']
    
    python_open_source_repositories_history = get_gcs_file_as_text(PYTHON_OPEN_SOURCE_REPOSITORIES_HISTORY_FILE)
    response_json = None 
    retry_count = 0

    while response_json is None:
        try:
            response = request_gemini(GeminiModels.GEMINI_2_5_PRO, daily_python_open_source_repositories_prompt(python_open_source_repositories_history))
            response_text = extract_outermost_braces(response.text)
            response_json = json.loads(response_text)
        except Exception as e:
            retry_count += 1
            if retry_count > 5:
                raise Exception("Failed to get daily AI papers")
            continue

    date = datetime.now().strftime("%Y-%m-%d")

    python_open_source_repositories_history += f"{response_json['title']}\n"
    upload_to_gcs_file(PYTHON_OPEN_SOURCE_REPOSITORIES_HISTORY_FILE, python_open_source_repositories_history)

    send_email(config['email'], f"[{date}] <Daily Python Open Source Repositories> {response_json['title']}", response_json['html_content'])

if __name__ == "__main__":
    get_daily_python_open_source_repositories() 
from py.llm_request.request_gemini import request_gemini, GeminiModels
from py.send_email import send_email
from py.prompts.daily_ai_paper import daily_ai_paper_prompt
from py.use_gcp_storage import get_gcs_file_as_text, upload_to_gcs_file
import json
import yaml
from datetime import datetime
from py.utils import extract_outermost_braces

PAPER_RECOMMENDATION_HISTORY_FILE = "paper_recommendation_history.txt"

with open('config/api_keys.yml', 'r') as file:
    api_keys = yaml.safe_load(file)

def get_daily_ai_papers():
    paper_recommendation_history = get_gcs_file_as_text(PAPER_RECOMMENDATION_HISTORY_FILE)
    response_json = None 
    retry_count = 0

    while response_json is None:
        try:
            response = request_gemini(GeminiModels.GEMINI_2_5_PRO, daily_ai_paper_prompt(paper_recommendation_history))
            response_text = extract_outermost_braces(response.text)
            response_json = json.loads(response_text)
        except Exception as e:
            retry_count += 1
            if retry_count > 5:
                raise Exception("Failed to get daily AI papers")
            continue

    date = datetime.now().strftime("%Y-%m-%d")

    paper_recommendation_history += f"{response_json['title']}\n"
    upload_to_gcs_file(PAPER_RECOMMENDATION_HISTORY_FILE, paper_recommendation_history)

    send_email(api_keys['email'], f"[{date}] <Daily AI Paper> {response_json['title']}", response_json['html_content'])

if __name__ == "__main__":
    get_daily_ai_papers()

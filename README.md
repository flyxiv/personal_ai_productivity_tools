# Personal AI Productivity Tools

A collection of AI-powered productivity tools for daily tasks.

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -e .
```

2. Configure API keys in `config/api_keys.yml`:
```yaml
resend_api_key: your_resend_api_key
gemini_api_key: your_gemini_api_key
email: your_email@example.com
```

3. Configure GCP settings in `config/gcp_config.yml`:
```yaml
bucket_name: your_gcp_bucket_name
```

### GitHub Actions Setup

The project includes a GitHub Actions workflow that runs daily at 1:00 AM UTC to fetch and email AI paper recommendations.

#### Required Secrets

Set up the following secrets in your GitHub repository (Settings > Secrets and variables > Actions):

1. **GEMINI_API_KEY**: Your Google Gemini API key
2. **RESEND_API_KEY**: Your Resend API key for sending emails
3. **EMAIL**: Your email address to receive daily papers
4. **GCP_CREDENTIALS_JSON**: Your Google Cloud service account credentials JSON
5. **GCP_BUCKET_NAME**: Your Google Cloud Storage bucket name

#### Setting up GCP Credentials

1. Create a service account in Google Cloud Console
2. Grant the service account Storage Object Admin role for your bucket
3. Download the JSON key file
4. Add the entire JSON content as the `GCP_CREDENTIALS_JSON` secret

## Usage

### Local Development

Run the daily AI papers script locally:
```bash
cd py
python jobs/daily_ai_papers.py
```

### GitHub Actions

The workflow will automatically run every day at 1:00 AM UTC. You can also manually trigger it from the Actions tab in your GitHub repository.

## Project Structure

- `py/` - Python source code
  - `jobs/` - Scheduled jobs
  - `llm_request/` - LLM API integrations
  - `prompts/` - Prompt templates
  - `send_email.py` - Email functionality
  - `use_gcp_storage.py` - Google Cloud Storage utilities
  - `utils.py` - Utility functions
- `config/` - Configuration files
- `.github/workflows/` - GitHub Actions workflows 
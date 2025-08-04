import yaml
import resend

with open('config/api_keys.yml', 'r') as file:
    api_keys = yaml.safe_load(file)


resend.api_key = api_keys['resend_api_key']

def send_email(to_email, email_title, email_html_content):
    resend.Emails.send({
        "from": "ns090200@resend.dev",
        "to": 'ns090200@gmail.com',
        "subject": email_title,
        "html": email_html_content
    })

if __name__ == "__main__":
    send_email(api_keys['email'], "Hello World", "<p>Congrats on sending your <strong>first email</strong>!</p>")
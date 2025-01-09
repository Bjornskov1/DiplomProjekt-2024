import requests
from msal import ConfidentialClientApplication
from django.conf import settings
from django.core.mail import EmailMessage

def send_email_via_graph_api(recipient_email, subject, body):
    try:
        # Use Django's EmailMessage to simulate sending email
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email="Meeting@angroupdk.onmicrosoft.com",
            to=[recipient_email]
        )
        email.send()  # This will use the console backend to print the email content
        print("Email content sent to console for debugging.")
        return True
    except Exception as e:
        print(f"Error in send_email_via_graph_api: {e}")
        return False


#def send_email_via_graph_api(recipient_email, subject, body):
#    try:
#        app = ConfidentialClientApplication(
#            client_id=settings.AZURE_CLIENT_ID,
#            client_credential=settings.AZURE_CLIENT_SECRET,
#            authority=f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}"
#        )
#        token_response = app.acquire_token_for_client(scopes=settings.AZURE_SCOPES)
#
#        if 'access_token' in token_response:
#            headers = {'Authorization': f"Bearer {token_response['access_token']}", 'Content-Type': 'application/json'}
#            email_data = {
#                "message": {
#                    "subject": subject,
#                    "body": {"contentType": "Text", "content": body},
#                    "toRecipients": [{"emailAddress": {"address": recipient_email}}],
#                },
#                "saveToSentItems": "false",
#            }
#            # Use the specific user's email for the endpoint
#            sender_email = "Meeting@angroupdk.onmicrosoft.com"  # Replace with the sender's email address
#            endpoint = f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"
#
#            response = requests.post(endpoint, headers=headers, json=email_data)
#            print(f"Email API Response: {response.status_code}, {response.text}")  # Debugging
#            return response.status_code == 202  # 202 means the request was accepted
#        else:
#            print(f"Failed to acquire token: {token_response}")
#           return False
#    except Exception as e:
#        print(f"Error in send_email_via_graph_api: {e}")
#        return False

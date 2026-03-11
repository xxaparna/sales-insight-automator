import os
import resend

resend.api_key = os.environ.get("RESEND_API_KEY")


def send_summary_email(recipient: str, summary: str, filename: str):

    formatted_summary = summary.replace("\n\n", "<br><br>")

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Sales Insight Report</h2>
            <p><b>File analyzed:</b> {filename}</p>
            <hr>
            <p>{formatted_summary}</p>
            <hr>
            <p style="font-size:12px;color:gray;">
            Generated automatically by Sales Insight Automator
            </p>
        </body>
    </html>
    """

    params = {
        "from": os.environ.get("EMAIL_FROM", "onboarding@resend.dev"),
        "to": [recipient],
        "subject": f"Sales Insights for {filename}",
        "html": html_content,
    }

    resend.Emails.send(params)
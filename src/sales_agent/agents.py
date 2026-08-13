import requests
from agents import Agent, ModelSettings, function_tool
from .config import MODEL_NAME, intro, pushover_token, pushover_url, pushover_user

instructions1 = intro + "Your email style is professional, serious, with gravitas and credibility."
instructions2 = intro + "Your email style is witty, engaging, and humorous."
instructions3 = intro + "Your email style is concise, to the point, in the style of a busy senior executive."

sales_agent1 = Agent(name="Professional Sales Agent", instructions=instructions1, model=MODEL_NAME)
sales_agent2 = Agent(name="Humorous Sales Agent", instructions=instructions2, model=MODEL_NAME)
sales_agent3 = Agent(name="Executive Sales Agent", instructions=instructions3, model=MODEL_NAME)


def push(message: str) -> None:
	print(f"Push: {message}")
	payload = {"user": pushover_user, "token": pushover_token, "message": message}
	requests.post(pushover_url, data=payload, timeout=10)


def send_message(subject: str, text_body: str, html_body: str) -> None:
	_ = html_body
	push(f"Subject: {subject}\n\n{text_body}")


@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
	"""
	Send out an email with the given subject and body to all sales prospects.

	Args:
		subject: The subject of the email.
		text_body: The body of the email as plain text.
		html_body: The HTML body of the email.
	"""
	send_message(subject, text_body, html_body)
	return "Email sent successfully"

decision = """
You pick the best cold sales email from the given options.
Imagine you are a customer and pick the one you are most likely to respond to.
Then use your tool to send the selected email.

After sending, reply in exactly this format:
Selected agent: <agent name>
Selected email:\n<full selected email>
"""

require_tool = ModelSettings(tool_choice="required")

sales_sender = Agent(
	name="Sales Sender",
	instructions=decision,
	model=MODEL_NAME,
	tools=[send_email_tool],
	model_settings=require_tool,
)
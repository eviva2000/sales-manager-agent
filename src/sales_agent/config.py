from dotenv import load_dotenv
import os

load_dotenv(override=True)

MODEL_NAME = "gpt-4o-mini"
pushover_user = os.getenv("PUSHOVER_USER", "")
pushover_token = os.getenv("PUSHOVER_TOKEN", "")
pushover_url = os.getenv("PUSHOVER_URL", "https://api.pushover.net/1/messages.json")

intro = """
You are a sales agent working for ComplAI,
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
You write emails.
"""
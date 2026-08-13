# Sales Agent

A small multi-agent workflow that writes, evaluates, and delivers a cold sales email for **ComplAI**, an AI-powered SaaS product for SOC 2 compliance and audit preparation.

Three agents draft the same outreach in different voices. A fourth agent chooses the option most likely to receive a response, then sends it through a Pushover-backed email simulator.

## How it works

1. The Professional, Humorous, and Executive sales agents generate cold-email drafts concurrently.
2. The Sales Sender reviews the three drafts and selects the strongest one from a prospect's perspective.
3. The sender must call `send_email_tool`, which posts the chosen subject and plain-text email to Pushover.
4. The command prints the three email titles, the selected agent, and a link to the OpenAI trace viewer.

The delivery integration is currently a simulator: it sends a Pushover notification rather than an email to real prospects. The HTML body is accepted by the tool for future email-provider integration, but is not used by the simulator.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key
- A Pushover application token and user key for delivery notifications

## Setup

Install the project dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_openai_api_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_application_token
# Optional: defaults to https://api.pushover.net/1/messages.json
PUSHOVER_URL=https://api.pushover.net/1/messages.json
```

Keep `.env` out of version control: it contains credentials.

## Run the workflow

```bash
uv run python -m sales_agent.main
```

Each run creates three draft emails, asks the sender agent to choose one, and sends the selected draft as a Pushover notification. OpenAI tracing is enabled for the workflow; the command prints the trace-viewer URL after it finishes.

## Project layout

```text
src/sales_agent/
├── agents.py        # Drafting agents, selection agent, and delivery tool
├── config.py        # Model and environment configuration
├── orchestrator.py  # Concurrent drafting and selection workflow
└── main.py          # Command-line entry point
```

## Customization

- Change `MODEL_NAME` in `src/sales_agent/config.py` to use another supported model.
- Adjust the product context and agent writing styles in `src/sales_agent/config.py` and `src/sales_agent/agents.py`.
- Replace `send_message` in `src/sales_agent/agents.py` with a real email-provider integration when ready to deliver to prospects.

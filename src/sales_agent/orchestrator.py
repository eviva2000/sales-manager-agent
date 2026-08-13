import asyncio
import re
from agents import Runner, trace
from .agents import sales_agent1, sales_agent2, sales_agent3, sales_sender


def _extract_title(email_text: str) -> str:
    for line in email_text.splitlines():
        clean_line = line.strip()
        if not clean_line:
            continue
        if clean_line.lower().startswith("subject:"):
            return clean_line.split(":", 1)[1].strip() or "(untitled)"
        return clean_line
    return "(untitled)"


async def run_workflow(message: str = "Write a cold sales email") -> dict[str, object]:
    with trace("Sales selection workflow with sending"):
        results = await asyncio.gather(
            Runner.run(sales_agent1, message),
            Runner.run(sales_agent2, message),
            Runner.run(sales_agent3, message),
        )
        outputs = [result.final_output for result in results]
        agent_names = [sales_agent1.name, sales_agent2.name, sales_agent3.name]
        titles = [_extract_title(email) for email in outputs]

        emails = "\n\n".join(
            [
                f"Email {i + 1} | Agent: {agent_names[i]}:\n\n{email}"
                for i, email in enumerate(outputs)
            ]
        )

        response = await Runner.run(
            sales_sender,
            "Choose and send one email from these options:\n\n"
            + emails
            + "\n\nWhen calling send_email_tool use:\n"
            + "- subject: first line or Subject line of selected email\n"
            + "- text_body: full selected email\n"
            + "- html_body: simple HTML wrapper around selected email",
        )

    response_text = str(response.final_output).strip()
    selected_agent_name = ""
    selected_email = ""

    selected_agent_match = re.search(r"Selected agent:\s*(.+)", response_text)
    if selected_agent_match:
        selected_agent_name = selected_agent_match.group(1).strip()

    selected_email_match = re.search(
        r"Selected email:\s*\n([\s\S]+)$", response_text
    )
    if selected_email_match:
        selected_email = selected_email_match.group(1).strip()

    selected_index = 0
    if selected_agent_name in agent_names:
        selected_index = agent_names.index(selected_agent_name)
    elif selected_email in outputs:
        selected_index = outputs.index(selected_email)

    if not selected_agent_name:
        selected_agent_name = agent_names[selected_index]
    if not selected_email:
        selected_email = outputs[selected_index]

    return {
        "selected_index": selected_index,
        "selected_agent_name": selected_agent_name,
        "titles": titles,
        "selected_email": selected_email,
    }
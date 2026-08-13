import asyncio
import re
from agents import Runner, trace
from .agents import sales_agent1, sales_agent2, sales_agent3, sales_picker


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
    with trace("Sales selection workflow"):
        results = await asyncio.gather(
            Runner.run(sales_agent1, message),
            Runner.run(sales_agent2, message),
            Runner.run(sales_agent3, message),
        )
        outputs = [result.final_output for result in results]
        agent_names = [sales_agent1.name, sales_agent2.name, sales_agent3.name]
        titles = [_extract_title(email) for email in outputs]

        emails = "\n\n".join(
            [f"Email {i + 1}:\n\n{email}" for i, email in enumerate(outputs)]
        )
        best = await Runner.run(
            sales_picker,
            "Pick the best option from the following emails:\n\n" + emails,
        )

    picker_text = str(best.final_output).strip()
    match = re.search(r"[123]", picker_text)
    selected_index = int(match.group()) - 1 if match else 0

    return {
        "selected_index": selected_index,
        "selected_agent_name": agent_names[selected_index],
        "titles": titles,
        "selected_email": outputs[selected_index],
    }
import asyncio
from .orchestrator import run_workflow

TRACE_URL = "https://platform.openai.com/logs?api=traces"


async def main():
    result = await run_workflow()
    selected_agent_name = result["selected_agent_name"]
    titles = result["titles"]
    selected_email = result["selected_email"]

    print("Email titles:")
    for i, title in enumerate(titles, start=1):
        print(f"{i}. {title}")

    print(f"\nSelected agent: {selected_agent_name}")
    print(f"Trace workflow URL: {TRACE_URL}")
    print(f"\nBest sales email:\n{selected_email}")


if __name__ == "__main__":
    asyncio.run(main())
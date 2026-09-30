import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.mcp_tool import (
    McpToolset,
    StdioConnectionParams,
)
from google.adk.agents.run_config import RunConfig
from google.genai import types
from mcp import StdioServerParameters


PROJECT_DIR = Path(__file__).resolve().parent

load_dotenv(PROJECT_DIR / ".env")

async def run_turn(
    runner: InMemoryRunner,
    user_id: str,
    session_id: str,
    user_text: str,
    run_config: RunConfig,
) -> None:
    user_message = types.UserContent(
        parts=[
            types.Part(
                text=user_text,
            ),
        ]
    )

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
        run_config=run_config,
    ):
        for function_call in event.get_function_calls():
            print(
                f"\n[tool call] {function_call.name}"
                f" {function_call.args}"
            )

        for function_response in event.get_function_responses():
            print(
                f"\n[tool result] {function_response.name}"
            )
            print(function_response.response)

        if event.is_final_response() and event.content:
            texts = [
                part.text
                for part in event.content.parts or []
                if part.text
            ]

            if texts:
                print("\nAgent >", "".join(texts))



async def main() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured in .env"
        )

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    connection = StdioConnectionParams(
        server_params=StdioServerParameters(
            command=str(PROJECT_DIR / ".venv/bin/mcp"),
            args=[
                "run",
                "main.py:mcp",
            ],
            cwd=PROJECT_DIR,
        ),
        timeout=5.0,
    )

    toolset = McpToolset(
        connection_params=connection,
        tool_filter=[
            "get_order",
        ],
    )

    agent = LlmAgent(
        name="support_agent",
        model=model,
        instruction=(
            "You are a customer support agent. "
            "Use the get_order tool whenever the user asks about "
            "a specific order. Never invent order information. "
            "Answer clearly and briefly."
        ),
        tools=[
            toolset,
        ],
    )

    app_name = "support_app"
    user_id = "student"

    async with InMemoryRunner(
            agent=agent,
            app_name=app_name,
    ) as runner:
        session = await runner.session_service.create_session(
            app_name=app_name,
            user_id=user_id,
        )

        run_config = RunConfig(
            max_llm_calls=4,
        )

        print("Support agent is ready.")
        print("Enter 'exit' to stop.")

        while True:
            user_text = await asyncio.to_thread(
                input,
                "\nYou > ",
            )

            user_text = user_text.strip()

            if user_text.lower() in {
                "exit",
                "quit",
            }:
                print("Goodbye.")
                break

            if not user_text:
                continue

            await run_turn(
                runner=runner,
                user_id=user_id,
                session_id=session.id,
                user_text=user_text,
                run_config=run_config,
            )

if __name__ == "__main__":
    asyncio.run(main())
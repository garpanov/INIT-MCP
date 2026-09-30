import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from workflow import run_support_workflow


PROJECT_DIR = Path(__file__).resolve().parent


async def main() -> None:
    server_parameters = StdioServerParameters(
        command=str(PROJECT_DIR / ".venv/bin/mcp"),
        args=[
            "run",
            "main.py:mcp",
        ],
        cwd=PROJECT_DIR,
    )

    async with stdio_client(
        server_parameters
    ) as (read_stream, write_stream):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await run_support_workflow(session)


if __name__ == "__main__":
    asyncio.run(main())
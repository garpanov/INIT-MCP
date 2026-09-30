import asyncio
from pathlib import Path

from google.adk.tools.mcp_tool import (
    McpToolset,
    StdioConnectionParams,
)
from mcp import StdioServerParameters


PROJECT_DIR = Path(__file__).resolve().parent


async def main() -> None:
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

    try:
        tools = await toolset.get_tools()

        print("Number of ADK tools:")
        print(len(tools))

        for tool in tools:
            print("\nADK tool type:")
            print(type(tool).__name__)

            print("\nTool name:")
            print(tool.name)

            print("\nTool description:")
            print(tool.description)

            print("\nOriginal MCP input schema:")
            print(tool.raw_mcp_tool.input_schema)

            declaration = tool._get_declaration()

            print("\nGemini function declaration:")
            print(
                declaration.model_dump(
                    exclude_none=True,
                    by_alias=True,
                )
            )
    finally:
        await toolset.close()


if __name__ == "__main__":
    asyncio.run(main())
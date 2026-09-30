import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from workflow import run_support_workflow


MCP_URL = "http://127.0.0.1:8000/mcp"


async def main() -> None:
    async with streamable_http_client(
        MCP_URL
    ) as (read_stream, write_stream):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await run_support_workflow(session)


if __name__ == "__main__":
    asyncio.run(main())
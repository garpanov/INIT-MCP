import unittest

from mcp.server.mcpserver.exceptions import ToolError

from main import mcp


class GetOrderTests(unittest.IsolatedAsyncioTestCase):
    async def test_existing_order_is_returned(self) -> None:
        result = await mcp.call_tool(
            "get_order",
            {
                "order_id": 123,
            },
        )

        self.assertFalse(result.is_error)
        self.assertEqual(
            result.structured_content,
            {
                "found": True,
                "order_id": 123,
                "status": "delivered",
                "product": "Headphones",
                "payment_status": "paid",
            },
        )

    async def test_missing_order_is_successful_result(self) -> None:
        result = await mcp.call_tool(
            "get_order",
            {
                "order_id": 999,
            },
        )

        self.assertFalse(result.is_error)
        self.assertEqual(
            result.structured_content,
            {
                "found": False,
                "order_id": 999,
                "status": None,
                "product": None,
                "payment_status": None,
            },
        )

    async def test_non_positive_order_id_is_rejected(self) -> None:
        with self.assertRaises(ToolError):
            await mcp.call_tool(
                "get_order",
                {
                    "order_id": 0,
                },
            )


if __name__ == "__main__":
    unittest.main()
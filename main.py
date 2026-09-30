from typing import Annotated

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field


from service import find_order


class OrderResult(BaseModel):
    found: bool
    order_id: int
    status: str | None = None
    product: str | None = None
    payment_status: str | None = None

mcp = MCPServer("support")


@mcp.tool(title="Get order", annotations=ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    idempotent_hint=True,
    open_world_hint=False
))
async def get_order(order_id: Annotated[int, Field(gt=0, description="Positive numeric order identifier")]) -> OrderResult:
    """
    Retrieve information about one specific order by its numeric ID.

    Use this when the customer provides an order ID and asks about
    the order status, purchased product, delivery, or payment status.

    Do not use this tool to search by customer name or email.
    This tool only reads order information; it cannot modify or cancel an order.
    """

    order = await find_order(order_id)

    if order is None:
        return OrderResult(
            found=False,
            order_id=order_id,
        )

    return OrderResult(
        found=True,
        **order,
    )

@mcp.resource(
    "company://refund-policy",
    title="Refund policy",
    description="Company rules for determining whether a purchase can be refunded.",
    mime_type="text/markdown",
)
async def refund_policy() -> str:
    return (
        "# Refund policy\n\n"
        "- Refunds are available within 30 days of purchase.\n"
        "- Electronics must not have physical damage.\n"
    )

@mcp.prompt(
    title="Customer support reply",
    description="Prepare instructions for a clear and concise customer support response.",
)
async def customer_support_reply(
        customer_name: Annotated[
            str,
            Field(
                min_length=1,
                description="Customer name used in the greeting",
            ),
        ],
        issue: Annotated[
            str,
            Field(
                min_length=1,
                description="Customer support issue that the response must address",
            ),
        ],
) -> str:
    return (
        "You are a customer support specialist.\n\n"
        f"Customer: {customer_name}\n"
        f"Issue: {issue}\n\n"
        "Respond clearly and briefly.\n"
    )
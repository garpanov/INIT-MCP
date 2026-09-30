from mcp import ClientSession


async def run_support_workflow(
    session: ClientSession,
) -> None:
    initialization = await session.initialize()

    print("Connected to server:")
    print(initialization.server_info.name)

    tools_result = await session.list_tools()
    resources_result = await session.list_resources()
    prompts_result = await session.list_prompts()

    print("\nTools:")
    for tool in tools_result.tools:
        print("-", tool.name)

    print("\nResources:")
    for resource in resources_result.resources:
        print("-", resource.uri)

    print("\nPrompts:")
    for prompt in prompts_result.prompts:
        print("-", prompt.name)

    order_result = await session.call_tool(
        "get_order",
        {
            "order_id": 123,
        },
    )

    print("\nOrder result:")

    if order_result.is_error:
        print("Tool failed:")
        print(order_result.content[0].text)
    else:
        print(order_result.structured_content)

    resource_result = await session.read_resource(
        "company://refund-policy"
    )

    print("\nRefund policy:")
    for content in resource_result.contents:
        print(content.text)

    prompt_result = await session.get_prompt(
        "customer_support_reply",
        {
            "customer_name": "Anna",
            "issue": "Order 456 has not arrived",
        },
    )

    print("\nPrompt:")
    for message in prompt_result.messages:
        print("Role:", message.role)
        print(message.content.text)
from src.utils.switchblade_decorator import tool


@tool(
    name="calculator",
    description="Adds two numbers",
    input_schema={
        "type": "object",
        "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        "required": ["a", "b"],
    },
    output_schema={"type": "object", "properties": {"result": {"type": "number"}}},
)
def add_numbers(args):
    return {"result": args["a"] + args["b"]}


@tool(
    name="multiply",
    description="Multiplies two numbers",
    input_schema={
        "type": "object",
        "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
    },
)
def mult_numbers(args):
    return {"result": args["a"] * args["b"]}

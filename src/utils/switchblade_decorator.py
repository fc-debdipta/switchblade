def tool(name, description, input_schema, output_schema=None):
    """
    Decorator to mark a function as a Switchblade tool.
    """

    def decorator(func):
        # Attach metadata directly to the function object
        func._is_switchblade_tool = True
        func._tool_metadata = {
            "name": name,
            "description": description,
            "input_schema": input_schema,
            "output_schema": output_schema or {},
        }
        return func

    return decorator

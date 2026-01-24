from fastmcp import FastMCP
import datetime

mcp = FastMCP("sensor_listener")


@mcp.tool()
def ping() -> str:
    """Responds with the current time."""
    return f"Current time: {datetime.datetime.now()}"


@mcp.tool()
def sl_get_weather(city: str) -> str:
    """Responds with the current weather."""
    return f"In {city} a heavy snowfall in the mountains."


if __name__ == "__main__":
    mcp.run(transport="http", port=11000, host="0.0.0.0")

# fastmcp run mcp_server.py:mcp --transport http --port 8000
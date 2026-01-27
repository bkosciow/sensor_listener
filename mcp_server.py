from fastmcp import FastMCP
import datetime
from node_listener.storage.storage import Storage
from node_listener.service.config import Config
from mcp_server.weather import weather
from mcp_server.air import air_quality

mcp = FastMCP("sensor_listener")
config = Config('config.ini')
Storage.set_engine(config.get_storage_engine())
storage = Storage()


@mcp.tool()
def ping() -> str:
    """Responds with the current time."""
    return f"Current time: {datetime.datetime.now()}"


@mcp.tool()
def sl_get_weather(city: str) -> str:
    """Responds with the current weather."""
    return f"Weather report:\n " + weather(storage.get('openweather'))


@mcp.tool()
def sl_get_air_quality() -> str:
    """Responds with air quality/pollution"""
    return "Air quality (index 0-5):\n" + air_quality(storage.get("openaq"))


if __name__ == "__main__":
    mcp.run(transport="http", port=11000, host="0.0.0.0")

# fastmcp run mcp_server.py:mcp --transport http --port 8000
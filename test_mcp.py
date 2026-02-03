from fastmcp import Client as MCPClient
import asyncio
import sys

MCP_SERVER_URL = "http://192.168.1.40:11000/mcp"


async def load_mcp_tools():
    """Connect to MCP server and get list of available tools"""
    async with MCPClient(MCP_SERVER_URL) as mcp:
        tools_list = await mcp.list_tools()

        return tools_list

    return tools_list


tools_list = asyncio.run(load_mcp_tools())
print(tools_list)

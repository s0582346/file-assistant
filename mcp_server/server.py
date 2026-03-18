import sys
from pathlib import Path

# Add project root to path so we can import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("receipt-extractor")

# Register tools
from mcp_server.tools import register_tools  # noqa: E402
register_tools(mcp)

if __name__ == "__main__":
    mcp.run()

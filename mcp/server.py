from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AgentHub", host="0.0.0.0", port=8000)

import tools.crm_tools
import tools.erp_tools
import tools.rh_tools

if __name__ == "__main__":
    mcp.run(transport="sse")
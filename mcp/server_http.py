from mcp.server.fastmcp import FastMCP
import httpx
import os

CRM_API_URL = os.getenv("CRM_API_URL", "http://localhost:8001")
ERP_API_URL = os.getenv("ERP_API_URL", "http://localhost:8002")
RH_API_URL = os.getenv("RH_API_URL", "http://localhost:8003")

mcp = FastMCP("AgentHub", host="0.0.0.0", port=8000)

import tools.crm_tools
import tools.erp_tools
import tools.rh_tools
    
if __name__ == "__main__":
    mcp.run()
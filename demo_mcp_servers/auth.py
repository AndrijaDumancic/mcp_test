import os
from fastmcp.server.auth import StaticTokenVerifier

MCP_AUTH_TOKEN = os.environ.get("MCP_AUTH_TOKEN", "demo-secret-token")

auth_provider = StaticTokenVerifier(
    tokens={
        MCP_AUTH_TOKEN: {
            "client_id": "mcp-client",
            "user": "mcp-user",
            "scopes": ["read", "write"]
        }
    }
)

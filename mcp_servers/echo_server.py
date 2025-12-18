from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="EchoServer",
    stateless_http=True,
    allowed_http_origins=["*"],
    enforce_host_header=False
)


@mcp.tool(description="A simple echo tool")
def echo(message: str) -> str:
    return f"Echo: {message}"
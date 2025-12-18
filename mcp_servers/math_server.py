from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="MathServer",
    stateless_http=True,
    allowed_http_origins=["*"],
    enforce_host_header=False
)


@mcp.tool(description="A simple add tool")
def add_two(n: int) -> int:
    return n + 2
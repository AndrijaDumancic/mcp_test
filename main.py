import contextlib
from fastapi import FastAPI
from demo_mcp_servers.bulk_chaining_mcp import mcp as bulk_chaining_mcp
from demo_mcp_servers.bulk_infinite_loop_mcp import mcp as infinite_loop_mcp
from demo_mcp_servers.issues_mcp import mcp as issues_mcp
import os


# Create the HTTP apps
bulk_chaining_app = bulk_chaining_mcp.http_app()
infinite_loop_app = infinite_loop_mcp.http_app()
issues_app = issues_mcp.http_app()


# Combined lifespan to manage all MCP session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(bulk_chaining_app.lifespan(bulk_chaining_app))
        await stack.enter_async_context(infinite_loop_app.lifespan(infinite_loop_app))
        await stack.enter_async_context(issues_app.lifespan(issues_app))
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/bulk_chaining", bulk_chaining_app)
app.mount("/infinite_loop", infinite_loop_app)
app.mount("/issues", issues_app)

PORT = os.environ.get("PORT", 10000)
HOST = os.environ.get("HOST", "0.0.0.0")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=int(PORT))
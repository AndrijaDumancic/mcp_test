import contextlib
import logging
import os
from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mcp_servers.echo_server import mcp as echo_mcp
from mcp_servers.math_server import mcp as math_mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verifies the Bearer token. 
    """
    expected_token = "my-super-secret-token"
    if credentials.credentials != expected_token:
        logger.warning("Authentication failed: Invalid token provided")
        raise HTTPException(
            status_code=401, 
            detail="Invalid authentication token"
        )
    return credentials.credentials

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting MCP servers...")
    async with contextlib.AsyncExitStack() as stack:
        # Run the session managers for the MCP servers
        await stack.enter_async_context(echo_mcp.session_manager.run())
        await stack.enter_async_context(math_mcp.session_manager.run())
        
        logger.info("All MCP servers are ready")
        yield
        logger.info("Shutting down MCP servers...")

# Main App
app = FastAPI(lifespan=lifespan)

# --- SECURE MOUNTING STRATEGY ---
# We create sub-FastAPI apps that HAVE the dependency, and mount the MCP app inside them.

# 1. Prepare Echo Server
echo_sub = FastAPI(dependencies=[Depends(verify_token)])
# FastMCP's streamable_http_app listens on /mcp by default relative to its mount.
# So mounting at "/" here means the path will be .../echo/mcp
echo_sub.mount("/", echo_mcp.streamable_http_app())

# 2. Prepare Math Server
math_sub = FastAPI(dependencies=[Depends(verify_token)])
math_sub.mount("/", math_mcp.streamable_http_app())

# 3. Mount the secured sub-apps to the main app
app.mount("/echo", echo_sub)
app.mount("/math", math_sub)
# --------------------------------

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "demo-mcp-servers"}

PORT = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting FastAPI server on 0.0.0.0:{PORT}")
    # Note: URLs will be:
    # http://.../echo/mcp
    # http://.../math/mcp
    uvicorn.run(app, host="0.0.0.0", port=PORT)
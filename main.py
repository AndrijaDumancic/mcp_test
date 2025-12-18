import contextlib
import logging
import os
from fastapi import FastAPI, Depends, HTTPException, Security
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
        await stack.enter_async_context(echo_mcp.session_manager.run())
        logger.info("Echo server started successfully")
        await stack.enter_async_context(math_mcp.session_manager.run())
        logger.info("Math server started successfully")
        logger.info("All MCP servers are ready")
        yield
        logger.info("Shutting down MCP servers...")

app = FastAPI(lifespan=lifespan, dependencies=[Depends(verify_token)])

@app.get("/health")
async def health_check():
    logger.debug("Health check requested")
    return {"status": "healthy", "service": "demo-mcp-servers"}

app.mount("/echo", echo_mcp.streamable_http_app())
app.mount("/math", math_mcp.streamable_http_app())



PORT = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting FastAPI server on 0.0.0.0:{PORT}")
    logger.info("Available endpoints (all require auth):")
    logger.info("  - GET  /health")
    logger.info("  - *    /echo/*")
    logger.info("  - *    /math/*")
    uvicorn.run(app, host="0.0.0.0", port=PORT)

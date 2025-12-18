import contextlib
import os
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mcp_servers.echo_server import mcp as echo_mcp
from mcp_servers.math_server import mcp as math_mcp

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    expected_token = "my-super-secret-token"
    
    if credentials.credentials != expected_token:
        raise HTTPException(
            status_code=401, 
            detail="Invalid authentication token"
        )
    return credentials.credentials

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(echo_mcp.session_manager.run())
        await stack.enter_async_context(math_mcp.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan, dependencies=[Depends(verify_token)])

@app.get("/health", dependencies=[])
async def health_check():
    return {"status": "healthy", "service": "demo-mcp-servers"}

app.mount("/echo", echo_mcp.streamable_http_app())
app.mount("/math", math_mcp.streamable_http_app())



PORT = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)

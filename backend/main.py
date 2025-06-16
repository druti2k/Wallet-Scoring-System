from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as api_router
from src.langchain_tools.assistant import handle_user_query
from fastapi.responses import JSONResponse
import traceback
import os
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Initialize any resources needed at startup
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Clean up resources on shutdown
    pass

# @app.post("/assistant/query")
# async def assistant_query(request: Request):
#     data = await request.json()
#     print("Received data:", data)  # Add this line
#     query = data.get("query")
#     if not query:
#         raise HTTPException(status_code=400, detail="Query is required")
#     try:
#         response = handle_user_query(query)
#         return {"response": response}
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))
            

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
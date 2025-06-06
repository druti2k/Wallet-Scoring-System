from fastapi import APIRouter, HTTPException, Request
from src.langchain_tools.assistant import handle_user_query

router = APIRouter()

@router.post("/assistant/query")
async def assistant_query(request: Request):
    data = await request.json()
    print("Received data:", data)
    query = data.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    try:
        print("Calling handle_user_query...")
        response = handle_user_query(query)
        print("Agent response:", response)
        return {"response": response}
    except Exception as e:
        print("Error in assistant_query:", e)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage

from ..oauth2 import get_current_user
from ..services.langgraph_agent import graph
from .. import schemas


router = APIRouter(
    prefix="/chat", 
    tags=["Chat"]
)  


@router.post("/", response_model=schemas.ChatResponse)
async def chat(
    payload: schemas.ChatRequest,
    current_user: int = Depends(get_current_user)
):
    # Create initial state with user_id
    state = {
        "messages": [HumanMessage(content=payload.query)],
    }
    config = {"configurable": {"thread_id": current_user.id}}   


    # Run graph with thread_id for memory persistence
    result = await graph.ainvoke(
        state,
        config=config
    )

    # Extract the last AI message
    ai_messages = [msg for msg in result["messages"] if msg.type == "ai"]
    
    if not ai_messages:
        return schemas.ChatResponse(response="No response generated")
    
    last_message = ai_messages[-1]
    
    # Extract text content
    if isinstance(last_message.content, str):
        response_text = last_message.content
    elif isinstance(last_message.content, list):
        text_parts = [
            block.get("text", "") 
            for block in last_message.content 
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        response_text = "".join(text_parts)
    else:
        response_text = str(last_message.content)

    return schemas.ChatResponse(response=response_text)
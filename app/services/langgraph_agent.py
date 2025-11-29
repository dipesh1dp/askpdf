from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState, StateGraph, END 
from langgraph.prebuilt import ToolNode, tools_condition 
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool 
from .vector_store import vector_store
from ..config import settings


# Initialize the model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0, 
    api_key=settings.gemini_api_key
)



graph_builder = StateGraph(MessagesState) 


# Retrieval tool 
@tool(response_format="content_and_artifact") 
def retrieve(query: str): 
    """Retrieve relevant documents from vector store"""
    try:
        # Check if vector store has documents
        if vector_store.index.ntotal == 0:
            return "No documents available in the knowledge base. Please upload documents first.", []
        
        retrieved_docs = vector_store.similarity_search(query, k=2)
        
        if not retrieved_docs:
            return "No relevant documents found for your query.", []
        
        serialized = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}" 
            for doc in retrieved_docs 
        )
        return serialized, retrieved_docs
    
    except Exception as e:
        return f"Error retrieving documents: {str(e)}", []


# Query node
async def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond""" 
    llm_with_tools = model.bind_tools([retrieve]) 
    response = await llm_with_tools.ainvoke(state["messages"])
    return {"messages": [response]} 


# Tool execution node 
tools = ToolNode([retrieve])


# Generate answer node
async def generate(state: MessagesState): 
    recent_tool_messages = [] 
    for message in reversed(state["messages"]): 
        if message.type == "tool": 
            recent_tool_messages.append(message)
        else:
            break 
    tool_messages = recent_tool_messages[::-1] 
    
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer concisely.\n\n"
        f"{docs_content}"
    )
    conversation_message = [
        msg for msg in state["messages"]
        if msg.type in ("human", "system") or 
           (msg.type == "ai" and not msg.tool_calls)
    ] 
    prompt = [SystemMessage(system_message_content)] + conversation_message
    response = await model.ainvoke(prompt) 
    return {"messages": [response]}


# Graph construction 
graph_builder.add_node(query_or_respond) 
graph_builder.add_node(tools)
graph_builder.add_node(generate) 

graph_builder.set_entry_point("query_or_respond") 
graph_builder.add_conditional_edges(
    "query_or_respond", 
    tools_condition, 
    {END: END, "tools": "tools"}
)
graph_builder.add_edge("tools", "generate") 
graph_builder.add_edge("generate", END) 

# In-memory checkpointer 
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)
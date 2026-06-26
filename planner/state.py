from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage


class PlannerState(TypedDict):
    """State object passed through the LangGraph workflow."""
    messages: Annotated[List[HumanMessage | AIMessage], "Conversation history"]

    destination: str
    days: str
    budget: str
    travelers: str
    travel_dates: str
    interests: List[str]
    accommodation: str
    transport: str
    pace: str

    itinerary: str

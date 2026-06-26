import os
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

from planner.state import PlannerState
from planner.prompts import itinerary_prompt


def get_llm():
    """Create the Groq-backed LLM. Reads the API key from the environment."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Add it to a .env file or your environment "
            "before running the app."
        )
    return ChatGroq(
        temperature=0,
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
    )


def build_collect_trip_details_node():
    """In the notebook this used input(). Here the Streamlit form already
    fills the state, so this node just records the conversation message."""

    def collect_trip_details(state: PlannerState) -> PlannerState:
        summary = f"""
Destination: {state['destination']}
Days: {state['days']}
Budget: {state['budget']}
Travelers: {state['travelers']}
Travel Dates: {state['travel_dates']}
Interests: {', '.join(state['interests'])}
Accommodation: {state['accommodation']}
Transport: {state['transport']}
Pace: {state['pace']}
"""
        return {
            **state,
            "messages": state["messages"] + [HumanMessage(content=summary)],
        }

    return collect_trip_details


def build_create_itinerary_node(llm):
    def create_itinerary(state: PlannerState) -> PlannerState:
        response = llm.invoke(
            itinerary_prompt.format_messages(
                destination=state["destination"],
                days=state["days"],
                budget=state["budget"],
                travelers=state["travelers"],
                travel_dates=state["travel_dates"],
                interests=", ".join(state["interests"]),
                accommodation=state["accommodation"],
                transport=state["transport"],
                pace=state["pace"],
            )
        )
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=response.content)],
            "itinerary": response.content,
        }

    return create_itinerary


def build_app():
    """Builds and compiles the LangGraph workflow. Call once per session."""
    llm = get_llm()

    workflow = StateGraph(PlannerState)
    workflow.add_node("collect_trip_details", build_collect_trip_details_node())
    workflow.add_node("create_itinerary", build_create_itinerary_node(llm))

    workflow.set_entry_point("collect_trip_details")
    workflow.add_edge("collect_trip_details", "create_itinerary")
    workflow.add_edge("create_itinerary", END)

    return workflow.compile()


def run_planner(trip_inputs: dict) -> str:
    """Run the compiled graph with the given trip inputs and return the itinerary text.

    trip_inputs keys: destination, days, budget, travelers, travel_dates,
    interests (list[str]), accommodation, transport, pace
    """
    app = build_app()

    initial_state: PlannerState = {
        "messages": [],
        "destination": trip_inputs["destination"],
        "days": trip_inputs["days"],
        "budget": trip_inputs["budget"],
        "travelers": trip_inputs["travelers"],
        "travel_dates": trip_inputs["travel_dates"],
        "interests": trip_inputs["interests"],
        "accommodation": trip_inputs["accommodation"],
        "transport": trip_inputs["transport"],
        "pace": trip_inputs["pace"],
        "itinerary": "",
    }

    final_state = None
    for output in app.stream(initial_state):
        final_state = output

    # app.stream yields {node_name: state} dicts; grab the last node's state
    last_node_state = list(final_state.values())[0]
    return last_node_state["itinerary"]

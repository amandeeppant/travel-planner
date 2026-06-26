import os
import streamlit as st
from dotenv import load_dotenv

from planner.graph import run_planner

load_dotenv()  # loads GROQ_API_KEY from a local .env file if present

st.set_page_config(page_title="AI Travel Planner", page_icon="🧳", layout="centered")

st.title("🧳 Intelligent Travel Planner")
st.caption("Powered by LangGraph + Groq (Llama 3.3 70B)")

# Warn early if the API key isn't configured, instead of failing mid-run
if not os.environ.get("GROQ_API_KEY"):
    st.warning(
        "GROQ_API_KEY is not set. Add it to a `.env` file in the project root "
        "(see `.env.example`) or as an environment variable, then restart the app."
    )

with st.form("trip_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("📍 Destination", placeholder="Goa, India")
        days = st.text_input("📅 Number of days", placeholder="4")
        budget = st.text_input("💰 Budget", placeholder="Low / Medium / Luxury or ₹ amount")
        travelers = st.text_input("👨‍👩‍👧 Number of travelers", placeholder="2")
    with col2:
        travel_dates = st.text_input("🗓 Travel dates / season", placeholder="Dec 2026")
        accommodation = st.selectbox(
            "🏨 Accommodation", ["Hotel", "Hostel", "Resort", "Homestay"]
        )
        transport = st.selectbox(
            "🚗 Preferred transport", ["Flight", "Train", "Bus", "Car"]
        )
        pace = st.selectbox("⚡ Trip pace", ["Relaxed", "Balanced", "Packed"])

    interests = st.text_input(
        "🎯 Interests (comma-separated)",
        placeholder="Adventure, Food, Beaches, Historical",
    )

    submitted = st.form_submit_button("Generate Itinerary ✈️")

if submitted:
    if not destination or not days:
        st.error("Please fill in at least the destination and number of days.")
    else:
        trip_inputs = {
            "destination": destination,
            "days": days,
            "budget": budget or "Not specified",
            "travelers": travelers or "Not specified",
            "travel_dates": travel_dates or "Flexible",
            "interests": [i.strip() for i in interests.split(",") if i.strip()] or ["General sightseeing"],
            "accommodation": accommodation,
            "transport": transport,
            "pace": pace,
        }

        with st.spinner("Planning your trip..."):
            try:
                itinerary = run_planner(trip_inputs)
                st.session_state["itinerary"] = itinerary
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if "itinerary" in st.session_state:
    st.markdown("---")
    st.subheader("Your Personalized Itinerary")
    st.markdown(st.session_state["itinerary"])
    st.download_button(
        "⬇️ Download as Markdown",
        st.session_state["itinerary"],
        file_name="itinerary.md",
    )

# Intelligent Travel Planner (Streamlit + LangGraph + Groq)

A simple Streamlit UI wrapped around the LangGraph travel-planning workflow
from the original notebook.

## Folder structure

```
travel_planner/
├── app.py                  # Streamlit UI (entry point)
├── requirements.txt
├── .env.example             # Copy to .env and add your real key
└── planner/
    ├── __init__.py
    ├── state.py             # PlannerState TypedDict
    ├── prompts.py           # Itinerary prompt template
    └── graph.py             # LangGraph workflow (collect_trip_details -> create_itinerary)
```

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Groq API key:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and paste your real key:
   ```
   GROQ_API_KEY=gsk_your_real_key
   ```

   ⚠️ **Security note:** the original notebook had a real Groq key hardcoded
   in the source. If that key is still active, revoke it in your Groq console
   and generate a new one — never commit `.env` to version control.

4. Run the app:
   ```bash
   streamlit run app.py
   ```

5. Open the URL Streamlit prints (usually `http://localhost:8501`), fill in
   the trip form, and click **Generate Itinerary**.

## How it maps to the notebook

- `PlannerState` → `planner/state.py`
- `itinerary_prompt` → `planner/prompts.py`
- `collect_trip_details` / `create_itinerary` nodes + `StateGraph` → `planner/graph.py`
- The notebook's `input()` calls and Gradio interface are both replaced by the
  Streamlit form in `app.py`, which collects the same fields (destination,
  days, budget, travelers, dates, interests, accommodation, transport, pace)
  and calls `run_planner(...)` to invoke the graph.

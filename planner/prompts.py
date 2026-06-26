from langchain_core.prompts import ChatPromptTemplate

itinerary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert AI Travel Planner.

Using the information provided by the user, create a complete personalized travel itinerary.

Include:

1. Trip Summary
2. Day-wise itinerary
3. Morning, Afternoon, Evening activities
4. Famous attractions
5. Food recommendations
6. Hotel recommendations according to budget
7. Estimated budget breakdown
8. Local transport suggestions
9. Packing tips
10. Safety tips
11. Best time to visit
12. Hidden gems
13. Nearby attractions

Keep the itinerary practical and realistic. Format the response in clean Markdown
with headings and bullet points so it renders nicely.
""",
        ),
        (
            "human",
            """
Destination: {destination}
Days: {days}
Budget: {budget}
Travelers: {travelers}
Travel Dates: {travel_dates}
Interests: {interests}
Accommodation: {accommodation}
Transport: {transport}
Trip Pace: {pace}
""",
        ),
    ]
)

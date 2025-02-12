import os
from fastapi import FastAPI, Query
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Mock flight response data
MOCK_FLIGHT_RESPONSE = [
    {
        "flight_number": "KQ101",
        "airline": "Kenya Airways",
        "departure": "NBO",
        "arrival": "KUL",
        "departure_time": "2025-02-15T10:00:00",
        "price": 750.00
    },
    {
        "flight_number": "EK202",
        "airline": "Emirates",
        "departure": "DXB",
        "arrival": "BOM",
        "departure_time": "2025-02-15T10:30:00",
        "price": 450.00
    }
]

@app.get("/search-flights")
async def search_flights(
    origin: str = Query(..., description="Origin airport code"),
    destination: str = Query(..., description="Destination airport code"),
    departure_date: str = Query(..., description="Departure date (YYYY-MM-DD)")
):
    """Returns a simpler JSON response for flight search queries."""
    try:
        print(f"🔹 Searching flights from {origin} to {destination} on {departure_date}")
        
        # Filter flights
        flights = [
            {
                "flight_number": flight["flight_number"],
                "airline": flight["airline"],
                "price": flight["price"],
                "departure_time": flight["departure_time"]
            }
            for flight in MOCK_FLIGHT_RESPONSE
            if flight["departure"] == origin and flight["arrival"] == destination
        ]

        if not flights:
            return {"message": f"No flights found from {origin} to {destination} on {departure_date}."}

        return {"flights": flights}
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": "Internal server error", "details": str(e)}

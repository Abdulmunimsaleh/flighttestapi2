import os
from fastapi import FastAPI, Query
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Mock flight response data
MOCK_FLIGHT_RESPONSE = {
    "flights": [
        {
            "flightNumber": "KQ101",
            "airline": "Kenya Airways",
            "departure": "NBO",
            "arrival": "KUL",
            "departureTime": "2025-02-15T10:00:00",
            "arrivalTime": "2025-02-15T22:00:00",
            "price": 750.00,
            "currency": "USD",
            "duration": "12h 00m",
            "stops": 0
        },
        {
            "flightNumber": "KQ102",
            "airline": "Kenya Airways",
            "departure": "KUL",
            "arrival": "NBO",
            "departureTime": "2025-02-20T08:00:00",
            "arrivalTime": "2025-02-20T20:00:00",
            "price": 750.00,
            "currency": "USD",
            "duration": "12h 00m",
            "stops": 0
        },
        {
            "flightNumber": "EK405",
            "airline": "Emirates",
            "departure": "DXB",
            "arrival": "BOM",
            "departureTime": "2025-03-15T14:00:00",
            "arrivalTime": "2025-03-15T18:30:00",
            "price": 450.00,
            "currency": "USD",
            "duration": "4h 30m",
            "stops": 0
        },
         {
            "flightNumber": "EK406",
            "airline": "Emirates",
            "departure": "BOM",
            "arrival": "DXB",
            "departureTime": "2025-04-20T16:00:00",
            "arrivalTime": "2025-04-20T20:30:00",
            "price": 450.00,
            "currency": "USD",
            "duration": "4h 30m",
            "stops": 0
        },
        {
            "flightNumber": "AI101",
            "airline": "Air India",
            "departure": "BOM",
            "arrival": "JFK",
            "departureTime": "2025-03-20T22:00:00",
            "arrivalTime": "2025-03-21T06:00:00",
            "price": 900.00,
            "currency": "USD",
            "duration": "14h 00m",
            "stops": 0
        },
         {
            "flightNumber": "AI102",
            "airline": "Air India",
            "departure": "JFK",
            "arrival": "BOM",
            "departureTime": "2025-04-15T23:00:00",
            "arrivalTime": "2025-04-16T09:00:00",
            "price": 900.00,
            "currency": "USD",
            "duration": "14h 00m",
            "stops": 0
        },
         {
            "flightNumber": "LH759",
            "airline": "Lufthansa",
            "departure": "BER",
            "arrival": "MBA",
            "departureTime": "2025-03-30T12:00:00",
            "arrivalTime": "2025-03-30T23:30:00",
            "price": 800.00,
            "currency": "USD",
            "duration": "11h 30m",
            "stops": 1
        },
          {
            "flightNumber": "LH760",
            "airline": "Lufthansa",
            "departure": "MBA",
            "arrival": "BER",
            "departureTime": "2025-04-05T07:00:00",
            "arrivalTime": "2025-04-05T18:30:00",
            "price": 800.00,
            "currency": "USD",
            "duration": "11h 30m",
            "stops": 1
        },
         {
            "flightNumber": "DL402",
            "airline": "Delta Airlines",
            "departure": "JFK",
            "arrival": "BER",
            "departureTime": "2025-03-25T08:00:00",
            "arrivalTime": "2025-03-25T18:00:00",
            "price": 750.00,
            "currency": "USD",
            "duration": "10h 00m",
            "stops": 1
        },
         {
            "flightNumber": "DL403",
            "airline": "Delta Airlines",
            "departure": "BER",
            "arrival": "JFK",
            "departureTime": "2025-04-10T10:00:00",
            "arrivalTime": "2025-04-10T20:00:00",
            "price": 750.00,
            "currency": "USD",
            "duration": "10h 00m",
            "stops": 1
        }
    ],
    "source": "Mock API"
}

@app.get("/search-flights")
async def search_flights(
    origin: str = Query(..., description="Origin airport code"),
    destination: str = Query(..., description="Destination airport code"),
    departure_date: str = Query(..., description="Departure date (YYYY-MM-DD)"),
    return_date: str = Query(None, description="Return date (YYYY-MM-DD), optional")):
    """Handles flight search requests and filters results based on user input, including round-trip flights."""
    try:
        print(f"🔹 Searching flights from {origin} to {destination} on {departure_date}")
        if return_date:
            print(f"🔹 Searching return flights from {destination} to {origin} on {return_date}")
        
        # Filter one-way flights
        outbound_flights = [
            flight for flight in MOCK_FLIGHT_RESPONSE["flights"]
            if flight["departure"] == origin and flight["arrival"] == destination
        ]

        # Filter return flights if return_date is provided
        return_flights = []
        if return_date:
            return_flights = [
                flight for flight in MOCK_FLIGHT_RESPONSE["flights"]
                if flight["departure"] == destination and flight["arrival"] == origin
            ]

        if not outbound_flights:
            return {"message": f"No flights found from {origin} to {destination} on {departure_date}."}
        
        response = {"outbound_flights": outbound_flights, "source": "Mock API"}
        if return_flights:
            response["return_flights"] = return_flights

        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": "Internal server error", "details": str(e)}

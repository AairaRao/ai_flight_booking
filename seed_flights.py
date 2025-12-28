from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to Local MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.flight_booking
    
    # Clear existing flights to avoid duplicates
    db.flights.delete_many({})
    print("Existing flights cleared.")

    airlines = ["SkyVoyage Air", "PIA", "AirSial", "SereneAir", "FlyJinnah"]
    local_cities = ["Karachi", "Lahore", "Islamabad", "Multan", "Peshawar"]
    international = ["Dubai", "London", "New York", "Istanbul", "Singapore"]

    flights_list = []

    # Generate 30 flights for year 2026
    for i in range(1, 31):
        is_intl = random.choice([True, False])
        from_c = random.choice(local_cities)
        
        # Ensure To and From are not the same
        if is_intl:
            to_c = random.choice(international)
        else:
            to_c = random.choice([c for c in local_cities if c != from_c])
        
        # Generate random dates throughout 2026
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Use 28 to avoid invalid dates
        flight_date = datetime(2026, month, day)
        
        flight_entry = {
            "flight_id": f"SV-{100 + i}",  # Consistent ID format for the badge
            "airline": random.choice(airlines),
            "from_city": from_c,
            "to_city": to_c,
            "base_price": random.randint(15000, 85000),
            "time": f"{random.randint(1, 12)}:{random.choice(['00', '30'])} {random.choice(['AM', 'PM'])}",
            "date": flight_date.strftime("%Y-%m-%d")
        }
        
        flights_list.append(flight_entry)
    
    # Also add some flights for the coming days (late December 2025 / early January 2026)
    for i in range(31, 41):
        is_intl = random.choice([True, False])
        from_c = random.choice(local_cities)
        
        if is_intl:
            to_c = random.choice(international)
        else:
            to_c = random.choice([c for c in local_cities if c != from_c])
        
        # Flights from now until next 30 days
        flight_date = datetime.now() + timedelta(days=random.randint(1, 30))
        
        flight_entry = {
            "flight_id": f"SV-{100 + i}",
            "airline": random.choice(airlines),
            "from_city": from_c,
            "to_city": to_c,
            "base_price": random.randint(15000, 85000),
            "time": f"{random.randint(1, 12)}:{random.choice(['00', '30'])} {random.choice(['AM', 'PM'])}",
            "date": flight_date.strftime("%Y-%m-%d")
        }
        
        flights_list.append(flight_entry)

    # Add a specific flight from Multan to London on Jan 1, 2026
    flights_list.append({
        "flight_id": "SV-2026",
        "airline": "SkyVoyage Air",
        "from_city": "Multan",
        "to_city": "London",
        "base_price": 85000,
        "time": "10:00 AM",
        "date": "2026-01-01"
    })
    
    # Insert into MongoDB
    db.flights.insert_many(flights_list)
    print(f"Successfully saved {len(flights_list)} flights to 'flight_booking.flights'.")
    
    # Print sample flights for verification
    print("\nSample Flight Entries:")
    for flight in flights_list[:5]:
        print(f"  {flight['flight_id']} | {flight['from_city']} -> {flight['to_city']} | {flight['date']} | Rs. {flight['base_price']}")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
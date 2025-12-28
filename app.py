from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
import re
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "skyvoyage_secret_key")

# MongoDB Connection - Uses environment variable for production, localhost for development
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/flight_booking")
mongo = PyMongo(app)

# ============================================
# MODULE 4: PRICING & AI ASSISTANT
# ============================================

# --- DISCOUNT RULES ---
DISCOUNT_RULES = {
    "WELCOME10": {"type": "percentage", "value": 10, "description": "Welcome discount - 10% off"},
    "SUMMER20": {"type": "percentage", "value": 20, "description": "Summer sale - 20% off"},
    "FLAT500": {"type": "fixed", "value": 500, "description": "Flat Rs. 500 off"},
    "FLAT1000": {"type": "fixed", "value": 1000, "description": "Flat Rs. 1000 off"},
    "EARLY15": {"type": "percentage", "value": 15, "description": "Early bird - 15% off"},
    "WEEKEND5": {"type": "percentage", "value": 5, "description": "Weekend special - 5% off"},
}

def calculate_price(base_price, promo_code=None, passengers=1):
    """
    Calculate final price with discounts applied.
    Returns dict with original_price, discount_amount, discount_description, final_price
    """
    original_price = base_price * passengers
    discount_amount = 0
    discount_description = None
    applied_code = None
    
    if promo_code and promo_code.upper() in DISCOUNT_RULES:
        rule = DISCOUNT_RULES[promo_code.upper()]
        applied_code = promo_code.upper()
        discount_description = rule["description"]
        
        if rule["type"] == "percentage":
            discount_amount = int(original_price * (rule["value"] / 100))
        elif rule["type"] == "fixed":
            discount_amount = rule["value"] * passengers
    
    final_price = max(original_price - discount_amount, 0)
    
    return {
        "original_price": original_price,
        "discount_amount": discount_amount,
        "discount_description": discount_description,
        "applied_code": applied_code,
        "final_price": final_price,
        "passengers": passengers
    }

# --- AI ASSISTANT KEYWORD MATCHING ---
def process_assistant_query(query):
    """
    Enhanced AI assistant for flight booking queries.
    Returns appropriate response based on keywords.
    """
    query_lower = query.lower().strip()
    
    # International flights query
    if "international" in query_lower:
        international_cities = ["Dubai", "London", "New York", "Istanbul", "Singapore"]
        flights = list(mongo.db.flights.find({"to_city": {"$in": international_cities}}).limit(5))
        if flights:
            flight_info = [f"✈️ {f['flight_id']}: {f['from_city']} → {f['to_city']} | Rs. {f['base_price']:,} | {f['date']}" for f in flights]
            return {
                "type": "flights",
                "message": "🌍 Here are some international flight options:",
                "data": flight_info,
                "suggestion": "Click on any flight in the search results to book it!"
            }
    
    # Domestic flights query
    if "domestic" in query_lower:
        local_cities = ["Karachi", "Lahore", "Islamabad", "Multan", "Peshawar"]
        flights = list(mongo.db.flights.find({
            "from_city": {"$in": local_cities},
            "to_city": {"$in": local_cities}
        }).limit(5))
        if flights:
            flight_info = [f"✈️ {f['flight_id']}: {f['from_city']} → {f['to_city']} | Rs. {f['base_price']:,}" for f in flights]
            return {
                "type": "flights",
                "message": "🏠 Here are domestic flight options within Pakistan:",
                "data": flight_info,
                "suggestion": "Domestic flights are usually cheaper and more frequent!"
            }
    
    # Cheapest/budget flights
    if any(word in query_lower for word in ["cheap", "cheapest", "budget", "affordable", "low cost", "best deal"]):
        flights = list(mongo.db.flights.find().sort("base_price", 1).limit(5))
        if flights:
            flight_info = [f"💰 {f['flight_id']}: {f['from_city']} → {f['to_city']} | Rs. {f['base_price']:,}" for f in flights]
            return {
                "type": "flights",
                "message": "💸 Here are our most affordable flights:",
                "data": flight_info,
                "suggestion": "Use promo code WELCOME10 for additional 10% off!"
            }
    
    # Business class query
    if "business" in query_lower and "class" in query_lower:
        return {
            "type": "info",
            "message": "✨ Business Class offers premium travel experience!",
            "data": [
                "🪑 Extra legroom and wider seats",
                "🍽️ Premium meal service",
                "💼 Priority boarding and baggage",
                "📱 In-flight entertainment",
                "💵 50% additional fare on base price"
            ],
            "suggestion": "Select 'Business' class during booking to upgrade your experience!"
        }
    
    # Family/children query
    if any(word in query_lower for word in ["family", "children", "kids", "infant", "baby"]):
        return {
            "type": "info",
            "message": "👨‍👩‍👧‍👦 Family Travel Information:",
            "data": [
                "👶 Infants (under 5): Get 5% discount on fare",
                "🧒 Children (5-11): Standard fare applies",
                "👨‍👩‍👧 Family bookings: Book all together for easier management",
                "🎒 Baggage: Each passenger gets standard allowance"
            ],
            "suggestion": "Book for all family members in one booking for convenience!"
        }
    
    # Trip planning
    if any(word in query_lower for word in ["plan", "planning", "trip", "vacation", "holiday", "getaway"]):
        return {
            "type": "info",
            "message": "🗺️ Let me help you plan your trip!",
            "data": [
                "🏖️ Beach getaway: Try Dubai or Singapore",
                "🏛️ Historical tours: Istanbul is perfect",
                "🌆 City exploration: London or New York",
                "🏔️ Local adventure: Islamabad or Peshawar"
            ],
            "suggestion": "Tell me your destination and I'll find the best flights!"
        }
    
    # Weekend getaway
    if "weekend" in query_lower:
        return {
            "type": "offers",
            "message": "🌟 Weekend Getaway Special!",
            "data": [
                "Use code WEEKEND5 for 5% off",
                "Popular weekend destinations: Dubai, Istanbul",
                "Short domestic trips: Lahore, Islamabad",
                "Book early for best prices!"
            ],
            "suggestion": "Search for flights and apply code WEEKEND5 at checkout!"
        }
    
    # Flight status
    if any(word in query_lower for word in ["status", "track", "where", "delayed"]):
        return {
            "type": "info",
            "message": "📊 Flight Status Information:",
            "data": [
                "Check your booking in 'My Bookings' section",
                "Flight updates are sent via email",
                "Contact airline for real-time updates",
                "Arrive 2-3 hours before departure"
            ],
            "suggestion": "Go to My Bookings to see your flight details."
        }
    
    # Flight search queries
    if any(word in query_lower for word in ["flight", "flights", "search", "find", "book", "show"]):
        # Check for specific destinations
        cities_to_check = {
            "dubai": "Dubai", "london": "London", "istanbul": "Istanbul", 
            "singapore": "Singapore", "new york": "New York",
            "karachi": "Karachi", "lahore": "Lahore", "islamabad": "Islamabad",
            "multan": "Multan", "peshawar": "Peshawar"
        }
        
        found_city = None
        for city_lower, city_proper in cities_to_check.items():
            if city_lower in query_lower:
                found_city = city_proper
                break
        
        if found_city:
            # Check if it's "from" or "to"
            if "from" in query_lower:
                flights = list(mongo.db.flights.find({"from_city": {"$regex": found_city, "$options": "i"}}).limit(5))
                direction = "from"
            else:
                flights = list(mongo.db.flights.find({"to_city": {"$regex": found_city, "$options": "i"}}).limit(5))
                direction = "to"
            
            if flights:
                flight_info = [f"✈️ {f['flight_id']}: {f['from_city']} → {f['to_city']} | Rs. {f['base_price']:,} | {f['date']}" for f in flights]
                return {
                    "type": "flights",
                    "message": f"🛫 Flights {direction} {found_city}:",
                    "data": flight_info,
                    "suggestion": f"Found {len(flights)} flights! Use the search page to see more options."
                }
            return {
                "type": "info",
                "message": f"No flights found {direction} {found_city} at the moment.",
                "suggestion": "Try searching with different dates on the home page."
            }
        
        # General flight search
        flights = list(mongo.db.flights.find().limit(5))
        if flights:
            flight_info = [f"✈️ {f['flight_id']}: {f['from_city']} → {f['to_city']} | Rs. {f['base_price']:,}" for f in flights]
            return {
                "type": "flights",
                "message": "🛫 Here are some available flights:",
                "data": flight_info,
                "suggestion": "Tell me a specific destination to narrow down results!"
            }
    
    # Pricing and discount queries
    if any(word in query_lower for word in ["price", "cost", "discount", "offer", "promo", "coupon", "code", "save"]):
        return {
            "type": "offers",
            "message": "🏷️ Current Discount Codes & Offers:",
            "data": [
                "🆕 WELCOME10 - 10% off for new users",
                "☀️ SUMMER20 - 20% off summer sale",
                "💵 FLAT500 - Rs. 500 flat discount",
                "💰 FLAT1000 - Rs. 1000 flat discount",
                "🌅 EARLY15 - 15% off early booking",
                "🗓️ WEEKEND5 - 5% weekend special"
            ],
            "suggestion": "Copy any code and apply at checkout! Infant travelers get automatic 5% off."
        }
    
    # Booking queries
    if any(word in query_lower for word in ["booking", "booked", "reservation", "my booking", "cancel", "my flight"]):
        if "user_id" in session:
            bookings = list(mongo.db.bookings.find({"user_id": ObjectId(session["user_id"])}).limit(5))
            if bookings:
                booking_info = []
                for b in bookings:
                    flight = mongo.db.flights.find_one({"_id": b.get("flight_id")})
                    if flight:
                        booking_info.append(f"📋 {flight['from_city']} → {flight['to_city']} | Rs. {b.get('final_price', 0):,} | {b.get('status', 'Booked')}")
                return {
                    "type": "bookings",
                    "message": f"📚 You have {len(bookings)} booking(s):",
                    "data": booking_info if booking_info else ["View details in My Bookings section"],
                    "suggestion": "Go to Profile > My Bookings for complete details."
                }
            return {
                "type": "info",
                "message": "📭 You don't have any bookings yet.",
                "suggestion": "Search for flights and book your next adventure! Use code WELCOME10 for 10% off."
            }
        return {
            "type": "info",
            "message": "🔐 Please login to view your bookings.",
            "suggestion": "Login or create an account to manage your bookings and get personalized offers!"
        }
    
    # Help queries
    if any(word in query_lower for word in ["help", "how", "what", "guide", "support", "can you"]):
        return {
            "type": "help",
            "message": "🤖 I'm your SkyVoyage AI Assistant! I can help you with:",
            "data": [
                "🔍 Search flights - 'Find flights to Dubai'",
                "💰 Get discounts - 'What promo codes are available?'",
                "📋 Check bookings - 'Show my bookings'",
                "💵 Compare prices - 'Show cheapest flights'",
                "✈️ Travel info - 'Tell me about business class'",
                "🗺️ Trip planning - 'Help me plan a trip'"
            ],
            "suggestion": "Just type your question naturally and I'll help you out!"
        }
    
    # Greeting
    if any(word in query_lower for word in ["hi", "hello", "hey", "good morning", "good evening", "howdy"]):
        name = session.get("name", "Traveler")
        return {
            "type": "greeting",
            "message": f"👋 Hello {name}! Welcome to SkyVoyage AI Assistant!",
            "data": [
                "I can search flights for you",
                "Show you the best discounts",
                "Help plan your trip",
                "Answer travel questions"
            ],
            "suggestion": "What would you like to do today? Try: 'Show flights to Dubai'"
        }
    
    # Thank you
    if any(word in query_lower for word in ["thank", "thanks", "appreciate"]):
        return {
            "type": "greeting",
            "message": "😊 You're welcome! Happy to help!",
            "suggestion": "Is there anything else I can assist you with?"
        }
    
    # Default response
    return {
        "type": "default",
        "message": "🤔 I'm not sure I understood that. Let me help you!",
        "data": [
            "Try: 'Search flights to Dubai'",
            "Try: 'What discounts are available?'",
            "Try: 'Show my bookings'",
            "Try: 'Help me plan a trip'"
        ],
        "suggestion": "Ask me about flights, discounts, bookings, or travel planning!"
    }

# --- AI ASSISTANT API ROUTE ---
@app.route('/assistant', methods=['POST'])
def assistant():
    """Process user query and return AI assistant response"""
    data = request.get_json()
    user_query = data.get('query', '')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    # Log user query to MongoDB (optional)
    mongo.db.assistant_logs.insert_one({
        "user_id": session.get("user_id"),
        "query": user_query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Process query and get response
    response = process_assistant_query(user_query)
    
    return jsonify(response)

# --- PRICE CALCULATION API ---
@app.route('/api/calculate_price', methods=['POST'])
def api_calculate_price():
    """API endpoint to calculate price with discounts"""
    data = request.get_json()
    base_price = data.get('base_price', 0)
    promo_code = data.get('promo_code', '')
    passengers = data.get('passengers', 1)
    
    result = calculate_price(base_price, promo_code, passengers)
    return jsonify(result)

# --- HOME PAGE ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_city = request.form.get('from_city')
        to_city = request.form.get('to_city')
        return redirect(url_for('results', from_city=from_city, to_city=to_city))
    return render_template('index.html')

# --- AI HELPER PAGE ---
@app.route('/ai-helper')
def ai_helper():
    return render_template('ai_helper.html')

# --- API: Search Flights for Index Page ---
@app.route('/api/search_flights')
def api_search_flights():
    from_city = request.args.get('from_city', '')
    to_city = request.args.get('to_city', '')
    date = request.args.get('date', '')
    
    query = {}
    
    if from_city:
        query["from_city"] = {"$regex": from_city, "$options": "i"}
    if to_city:
        query["to_city"] = {"$regex": to_city, "$options": "i"}
    if date:
        query["date"] = date
    
    flights = list(mongo.db.flights.find(query))
    
    # Convert ObjectId to string and format for frontend
    formatted_flights = []
    for flight in flights:
        formatted_flights.append({
            "_id": str(flight["_id"]),
            "airline": flight.get("airline", "SkyVoyage Air"),
            "airlineCode": flight.get("airline", "SkyVoyage Air")[:2].upper(),
            "flightNumber": flight.get("flight_id", "SV-100"),
            "departure": {
                "time": flight.get("time", "09:00 AM"),
                "city": flight.get("from_city", ""),
                "code": flight.get("from_city", "")[:3].upper()
            },
            "arrival": {
                "time": calculate_arrival_time(flight.get("time", "09:00 AM")),
                "city": flight.get("to_city", ""),
                "code": flight.get("to_city", "")[:3].upper()
            },
            "duration": calculate_duration(flight.get("from_city", ""), flight.get("to_city", "")),
            "stops": "Non-stop" if flight.get("base_price", 0) > 30000 else "1 Stop",
            "price": flight.get("base_price", 0),
            "date": flight.get("date", "")
        })
    
    return jsonify(formatted_flights)

def calculate_arrival_time(departure_time):
    """Calculate a rough arrival time (add 3-5 hours)"""
    try:
        parts = departure_time.split()
        time_part = parts[0]
        period = parts[1] if len(parts) > 1 else "AM"
        hour, minute = map(int, time_part.split(':'))
        
        # Add 3-4 hours for flight duration
        hour = (hour + 3) % 12
        if hour == 0:
            hour = 12
        
        # Toggle AM/PM if crossing noon
        if hour < 4:
            period = "PM" if period == "AM" else "AM"
            
        return f"{hour}:{minute:02d} {period}"
    except:
        return "12:00 PM"

def calculate_duration(from_city, to_city):
    """Calculate estimated flight duration"""
    international = ["Dubai", "London", "New York", "Istanbul", "Singapore"]
    if to_city in international or from_city in international:
        return f"{3 + (hash(from_city + to_city) % 3)}h {30 if hash(to_city) % 2 else 0}m"
    return f"{1 + (hash(from_city + to_city) % 2)}h {30 if hash(to_city) % 2 else 0}m"

# --- RESULTS PAGE ---
@app.route('/results')
def results():
    from_city = request.args.get('from_city')
    to_city = request.args.get('to_city')
    
    # --- FILTER LOGIC FOR SIDEBAR ---
    selected_airlines = request.args.getlist('airlines')  # For Airline checkboxes
    max_price = request.args.get('price_range')          # For Price slider
    
    query = {}
    
    # Text Search Logic
    if from_city: 
        query["from_city"] = {"$regex": from_city, "$options": "i"}
    if to_city: 
        query["to_city"] = {"$regex": to_city, "$options": "i"}
        
    # Apply Airline Filter if any are selected
    if selected_airlines:
        query["airline"] = {"$in": selected_airlines}
        
    # Apply Price Filter if slider is used
    if max_price:
        try:
            query["base_price"] = {"$lte": int(max_price)}
        except ValueError:
            pass # Handle cases where max_price might not be an integer

    # Fetching real data from MongoDB flights collection
    flights = list(mongo.db.flights.find(query))
    return render_template('results.html', flights=flights)

# --- AUTHENTICATION ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if mongo.db.users.find_one({"email": email}):
            flash("Email already exists!", "error")
        else:
            mongo.db.users.insert_one({
                "name": name,
                "email": email,
                "password": generate_password_hash(password)
            })
            flash("Account created! Please login.", "success")
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = mongo.db.users.find_one({"email": email})
        
        if user and user.get('password') and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['name'] = user['name']
            return redirect(url_for('profile'))
        else:
            flash("Invalid email or password", "error")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', name=session['name'])

# --- PASSWORD RECOVERY ---
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = mongo.db.users.find_one({"email": email})
        
        if user:
            # In a real app, you'd send an email with a reset link
            # For this demo, we'll redirect directly to reset page
            return redirect(url_for('reset_password', email=email))
        else:
            flash("No account found with that email address", "error")
    
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email') or request.form.get('email')
    
    if not email:
        flash("Invalid reset request", "error")
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('reset_password.html', email=email)
        
        if len(password) < 6:
            flash("Password must be at least 6 characters", "error")
            return render_template('reset_password.html', email=email)
        
        # Update password in database
        result = mongo.db.users.update_one(
            {"email": email},
            {"$set": {"password": generate_password_hash(password)}}
        )
        
        if result.modified_count > 0:
            flash("Password reset successful! Please login with your new password.", "success")
            return redirect(url_for('login'))
        else:
            flash("Error resetting password. Please try again.", "error")
    
    return render_template('reset_password.html', email=email)

# --- SETTINGS ---
@app.route('/settings')
def settings():
    if 'user_id' not in session:
        flash("Please login to access settings", "info")
        return redirect(url_for('login'))
    
    user = mongo.db.users.find_one({"_id": ObjectId(session['user_id'])})
    return render_template('settings.html', user=user)

@app.route('/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Validate
    if new_password != confirm_password:
        flash("New passwords do not match", "error")
        return redirect(url_for('settings'))
    
    if len(new_password) < 6:
        flash("Password must be at least 6 characters", "error")
        return redirect(url_for('settings'))
    
    # Verify current password
    user = mongo.db.users.find_one({"_id": ObjectId(session['user_id'])})
    
    if not user or not check_password_hash(user['password'], current_password):
        flash("Current password is incorrect", "error")
        return redirect(url_for('settings'))
    
    # Update password
    mongo.db.users.update_one(
        {"_id": ObjectId(session['user_id'])},
        {"$set": {"password": generate_password_hash(new_password)}}
    )
    
    flash("Password updated successfully!", "success")
    return redirect(url_for('settings'))

@app.route('/delete-account')
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = ObjectId(session['user_id'])
    
    # Delete user's bookings
    mongo.db.bookings.delete_many({"user_id": user_id})
    
    # Delete user account
    mongo.db.users.delete_one({"_id": user_id})
    
    # Clear session
    session.clear()
    
    flash("Your account has been deleted successfully", "success")
    return redirect(url_for('index'))

# --- MODULE 3: BOOKING SYSTEM ROUTES ---

@app.route('/confirm_booking/<flight_id>')
def confirm_booking(flight_id):
    if 'user_id' not in session:
        flash("Please login to book a flight", "info")
        return redirect(url_for('login'))
    
    # Fetch specific flight using its MongoDB ObjectId
    try:
        flight = mongo.db.flights.find_one({"_id": ObjectId(flight_id)})
    except:
        flash("Invalid flight ID", "error")
        return redirect(url_for('index'))
    
    if not flight:
        flash("Flight not found", "error")
        return redirect(url_for('index'))
    
    # Pass available discount codes to template
    available_discounts = [
        {"code": "WELCOME10", "description": "10% off for new users"},
        {"code": "SUMMER20", "description": "20% summer sale"},
        {"code": "FLAT500", "description": "Rs. 500 flat off"},
        {"code": "EARLY15", "description": "15% early bird discount"},
    ]
    
    return render_template('confirm_booking.html', flight=flight, discounts=available_discounts)

@app.route('/book_flight/<flight_id>', methods=['POST'])
def book_flight_action(flight_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        flight = mongo.db.flights.find_one({"_id": ObjectId(flight_id)})
    except:
        flash("Invalid flight ID", "error")
        return redirect(url_for('index'))
    
    if not flight:
        flash("Flight not found", "error")
        return redirect(url_for('index'))
    
    # Get booking details from form
    promo_code = request.form.get('promo_code', '')
    adults = int(request.form.get('adults', 1))
    children = int(request.form.get('children', 0))
    infants = int(request.form.get('infants', 0))
    travel_class = request.form.get('travel_class', 'economy')
    
    # Calculate price with all factors
    base_price = flight['base_price']
    class_multiplier = 1.5 if travel_class == 'business' else 1.0
    price_per_person = base_price * class_multiplier
    
    # Calculate totals
    adult_total = price_per_person * adults
    child_total = price_per_person * children
    infant_full = price_per_person * infants
    infant_discount = infant_full * 0.05  # 5% off for infants under 5
    infant_total = infant_full - infant_discount
    
    subtotal = adult_total + child_total + infant_total
    total_passengers = adults + children + infants
    
    # Apply promo discount
    promo_discount = 0
    if promo_code:
        promo_code = promo_code.upper()
        if promo_code in DISCOUNT_RULES:
            rule = DISCOUNT_RULES[promo_code]
            if rule["type"] == "percentage":
                promo_discount = subtotal * (rule["value"] / 100)
            else:
                promo_discount = min(rule["value"] * total_passengers, subtotal)
    
    final_price = subtotal - promo_discount
    total_discount = infant_discount + promo_discount
    
    # Create the Booking Record with all details
    booking_data = {
        "user_id": ObjectId(session['user_id']),
        "flight_id": ObjectId(flight_id),
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "adults": adults,
        "children": children,
        "infants": infants,
        "total_passengers": total_passengers,
        "travel_class": travel_class,
        "base_price_per_person": price_per_person,
        "original_price": adult_total + child_total + infant_full,
        "infant_discount": infant_discount,
        "promo_discount": promo_discount,
        "discount_code": promo_code if promo_discount > 0 else None,
        "total_discount": total_discount,
        "final_price": final_price,
        "status": "Booked"
    }
    
    mongo.db.bookings.insert_one(booking_data)
    
    if total_discount > 0:
        flash(f"Flight Booked! You saved Rs. {int(total_discount):,}!", "success")
    else:
        flash("Flight Booked Successfully!", "success")
    
    return redirect(url_for('my_bookings'))

@app.route('/my_bookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_bookings = list(mongo.db.bookings.find({"user_id": ObjectId(session['user_id'])}))
    
    # "Join" flight info to show details in the table
    for booking in user_bookings:
        flight_details = mongo.db.flights.find_one({"_id": booking['flight_id']})
        booking['flight_info'] = flight_details 
        
    return render_template('my_bookings.html', bookings=user_bookings)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
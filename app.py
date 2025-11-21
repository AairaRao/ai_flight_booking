from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/flight_booking_db"
mongo = PyMongo(app)
users_collection = mongo.db.users


@app.route("/")
def index():
    # simple home page with a link to signup
    return """
    <html>
      <head>
        <title>Flight Booking - Home</title>
      </head>
      <body style="font-family: Arial; background-color: #f4f4f4;">
        <h1>HOME PAGE IS WORKING 🎉</h1>
        <p>Welcome to the Flight Booking Website.</p>
        <a href="/signup">Go to Sign Up</a>
      </body>
    </html>
    """


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # just to see in terminal
        print("Form submitted:", name, email, password)

        # basic validation
        if not name or not email or not password:
            return """
            <html>
              <body style="font-family: Arial;">
                <h2>Error: Please fill all fields.</h2>
                <a href="/signup">Back to Sign Up</a>
              </body>
            </html>
            """

        # check if email already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return f"""
            <html>
              <body style="font-family: Arial;">
                <h2>Error: This email is already registered.</h2>
                <p>Email: {email}</p>
                <a href="/signup">Try another email</a><br>
                <a href="/">Back to Home</a>
              </body>
            </html>
            """

        # hash password for safety
        hashed_password = generate_password_hash(password)

        # insert into MongoDB
        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

        return f"""
        <html>
          <head><title>Signup Success</title></head>
          <body style="font-family: Arial; background-color: #f4f4f4;">
            <h2>Account Created Successfully! 🎉</h2>
            <p>Name: {name}</p>
            <p>Email: {email}</p>
            <a href="/">Back to Home</a>
          </body>
        </html>
        """

    # if GET, show form
    return """
    <html>
      <head>
        <title>Flight Booking - Sign Up</title>
      </head>
      <body style="font-family: Arial; background-color: #f4f4f4;">
        <h2>Create Account</h2>
        <form method="POST" action="/signup">
          <label>Name:</label><br>
          <input type="text" name="name" required><br><br>

          <label>Email:</label><br>
          <input type="email" name="email" required><br><br>

          <label>Password:</label><br>
          <input type="password" name="password" required><br><br>

          <button type="submit">Sign Up</button>
        </form>
        <br>
        <a href="/">Back to Home</a>
      </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)

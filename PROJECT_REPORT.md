# SkyVoyage - Flight Booking System
## Comprehensive Project Report

---

## 📋 Table of Contents
1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Technologies Used](#4-technologies-used)
5. [System Architecture](#5-system-architecture)
6. [Database Design](#6-database-design)
7. [Modules & Features](#7-modules--features)
8. [User Interface Design](#8-user-interface-design)
9. [API Endpoints](#9-api-endpoints)
10. [Security Features](#10-security-features)
11. [Future Enhancements](#11-future-enhancements)
12. [Conclusion](#12-conclusion)

---

## 1. Project Overview

**Project Name:** SkyVoyage - Premium Flight Booking System  
**Project Type:** Web Application  
**Domain:** Travel & Transportation  
**Development Period:** December 2025  

SkyVoyage is a comprehensive flight booking web application that allows users to search, compare, and book flights both domestically within Pakistan and internationally. The system features an AI-powered assistant, dynamic pricing with promotional discounts, and a fully responsive design that works seamlessly across all device sizes.

---

## 2. Problem Statement

### Current Challenges in Flight Booking:
1. **Complex Booking Process:** Traditional flight booking systems often have complicated interfaces that confuse users.
2. **Lack of Real-time Assistance:** Users frequently need help but don't have access to immediate support.
3. **Static Pricing:** Many systems don't offer dynamic discounts or promotional offers.
4. **Limited Accessibility:** Older systems are not mobile-friendly, limiting user access.
5. **No Personalization:** Users don't get personalized recommendations based on their preferences.

### Solution Provided:
SkyVoyage addresses these challenges by providing:
- An intuitive, modern user interface
- An AI-powered chatbot for instant assistance
- Dynamic pricing with multiple promotional codes
- Fully responsive design for all devices
- Personalized user accounts with booking history

---

## 3. Objectives

### Primary Objectives:
1. ✅ Develop a user-friendly flight search and booking platform
2. ✅ Implement secure user authentication and account management
3. ✅ Create an AI assistant for customer support
4. ✅ Enable dynamic pricing with promotional discounts
5. ✅ Ensure responsive design for all screen sizes

### Secondary Objectives:
1. ✅ Support multiple passenger types (Adults, Children, Infants)
2. ✅ Offer Economy and Business class options
3. ✅ Provide multi-city flight booking capability
4. ✅ Implement dark/light theme toggle
5. ✅ Enable voice input for AI assistant

---

## 4. Technologies Used

### Backend Technologies:
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Primary programming language |
| Flask | 3.1.2 | Web framework |
| Flask-PyMongo | 3.0.1 | MongoDB integration |
| PyMongo | 4.15.4 | MongoDB driver |
| Werkzeug | 3.1.3 | Password hashing & security |
| Jinja2 | 3.1.6 | Template engine |
| Gunicorn | 23.0.0 | Production WSGI server |

### Frontend Technologies:
| Technology | Purpose |
|------------|---------|
| HTML5 | Page structure |
| CSS3 | Styling & animations |
| JavaScript (ES6+) | Interactivity & API calls |
| Font Awesome 6.4 | Icons |
| Web Speech API | Voice input/output for AI |

### Database:
| Technology | Purpose |
|------------|---------|
| MongoDB | NoSQL database for flexible data storage |

---

## 5. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Desktop │  │ Tablet  │  │ Mobile  │  │ Browser │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
└───────┼────────────┼────────────┼────────────┼──────────────┘
        │            │            │            │
        └────────────┴─────┬──────┴────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Jinja2 Templates (HTML/CSS/JS)          │    │
│  │  • base.html (Layout)    • index.html (Home)         │    │
│  │  • login.html           • signup.html                │    │
│  │  • profile.html         • settings.html              │    │
│  │  • confirm_booking.html • my_bookings.html           │    │
│  │  • ai_helper.html       • results.html               │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Flask Application (app.py)          │    │
│  │  ┌───────────────┐  ┌───────────────┐               │    │
│  │  │ Authentication │  │ Flight Search │               │    │
│  │  │    Module      │  │    Module     │               │    │
│  │  └───────────────┘  └───────────────┘               │    │
│  │  ┌───────────────┐  ┌───────────────┐               │    │
│  │  │    Booking    │  │  AI Assistant │               │    │
│  │  │    Module     │  │    Module     │               │    │
│  │  └───────────────┘  └───────────────┘               │    │
│  │  ┌───────────────┐  ┌───────────────┐               │    │
│  │  │    Pricing    │  │   Settings    │               │    │
│  │  │    Module     │  │    Module     │               │    │
│  │  └───────────────┘  └───────────────┘               │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  MongoDB Database                    │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────────┐  │    │
│  │  │  users  │ │ flights │ │bookings │ │asst_logs  │  │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └───────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Database Design

### Collections Structure:

#### 6.1 Users Collection
```javascript
{
  "_id": ObjectId,
  "name": String,
  "email": String (unique),
  "password": String (hashed),
  "created_at": DateTime
}
```

#### 6.2 Flights Collection
```javascript
{
  "_id": ObjectId,
  "flight_id": String,        // e.g., "SV-101"
  "airline": String,          // e.g., "SkyVoyage Air"
  "from_city": String,        // e.g., "Karachi"
  "to_city": String,          // e.g., "Dubai"
  "base_price": Number,       // e.g., 45000
  "time": String,             // e.g., "10:00 AM"
  "date": String              // e.g., "2026-01-15"
}
```

#### 6.3 Bookings Collection
```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "flight_id": ObjectId,
  "booking_date": String,
  "adults": Number,
  "children": Number,
  "infants": Number,
  "total_passengers": Number,
  "travel_class": String,     // "economy" or "business"
  "base_price_per_person": Number,
  "original_price": Number,
  "infant_discount": Number,
  "promo_discount": Number,
  "discount_code": String,
  "total_discount": Number,
  "final_price": Number,
  "status": String            // "Booked"
}
```

#### 6.4 Assistant Logs Collection
```javascript
{
  "_id": ObjectId,
  "user_id": String,
  "query": String,
  "timestamp": String
}
```

---

## 7. Modules & Features

### Module 1: User Authentication System
| Feature | Description |
|---------|-------------|
| Sign Up | New user registration with email validation |
| Login | Secure authentication with password hashing |
| Logout | Session termination |
| Forgot Password | Password recovery via email verification |
| Reset Password | Set new password functionality |
| Change Password | Update password from settings |
| Delete Account | Permanent account deletion |

### Module 2: Flight Search & Display
| Feature | Description |
|---------|-------------|
| Search Form | Origin, destination, date, passengers selection |
| One-way Search | Single trip flight search |
| Multi-city Search | Multiple leg journey booking |
| Filter Options | Airline, price range, stops, time filters |
| Sort Options | Sort by price, duration, departure time |
| Flight Cards | Detailed flight information display |

### Module 3: Booking System
| Feature | Description |
|---------|-------------|
| Passenger Selection | Adults, Children (5-11), Infants (<5 years) |
| Class Selection | Economy and Business class options |
| Price Calculation | Dynamic pricing based on passengers & class |
| Promo Codes | Multiple discount codes support |
| Infant Discount | Automatic 5% off for infants |
| Booking Confirmation | Detailed booking summary |
| My Bookings | View all past and current bookings |

### Module 4: AI Assistant
| Feature | Description |
|---------|-------------|
| Natural Language Processing | Keyword-based query understanding |
| Flight Search | Search flights via chat commands |
| Discount Information | Get available promo codes |
| Booking Status | Check existing bookings |
| Travel Recommendations | Trip planning suggestions |
| Voice Input | Speech-to-text support |
| Voice Output | Text-to-speech responses |
| Quick Actions | Pre-defined query buttons |

### Module 5: Pricing & Discounts
| Promo Code | Type | Value | Description |
|------------|------|-------|-------------|
| WELCOME10 | Percentage | 10% | Welcome discount for new users |
| SUMMER20 | Percentage | 20% | Summer sale discount |
| FLAT500 | Fixed | Rs. 500 | Flat discount per passenger |
| FLAT1000 | Fixed | Rs. 1000 | Flat discount per passenger |
| EARLY15 | Percentage | 15% | Early bird booking discount |
| WEEKEND5 | Percentage | 5% | Weekend special offer |

### Module 6: Settings & Preferences
| Feature | Description |
|---------|-------------|
| Profile Information | View name, email, member since |
| Change Password | Update password securely |
| Dark Mode Toggle | Switch between light/dark themes |
| Email Notifications | Toggle booking updates |
| Promotional Emails | Toggle offer notifications |
| Account Deletion | Remove account permanently |

---

## 8. User Interface Design

### Design Principles:
1. **Modern & Clean:** Blue-themed professional design
2. **Responsive:** Works on all screen sizes (mobile-first approach)
3. **Accessible:** Clear typography, proper contrast
4. **Intuitive:** Easy navigation, clear call-to-actions

### Color Palette:
| Color | Hex Code | Usage |
|-------|----------|-------|
| Primary Blue | #1A73E8 | Buttons, links, accents |
| Light Blue | #4A9DFF | Gradients, hover states |
| Background Light | #E7F1FF | Light mode background |
| Background Dark | #0B1F3B | Dark mode background |
| Text Primary | #0B1F3B | Headings, body text |
| Text Secondary | #666666 | Subtitles, hints |
| Error Red | #FF4757 | Error messages, danger zone |
| Success Green | #2E7D32 | Success messages |

### Responsive Breakpoints:
| Breakpoint | Target |
|------------|--------|
| 1400px+ | Large desktops |
| 1024px | Tablets landscape |
| 768px | Tablets portrait |
| 480px | Mobile devices |
| 500px height | Landscape mobile |

### Key UI Components:
- **Hero Section:** Animated world map with flight paths
- **Search Card:** Tab-based trip type selection
- **Flight Cards:** Airline info, route, duration, price
- **Passenger Dropdown:** Modal-style selector
- **Filter Sidebar:** Slide-out filter panel
- **AI Chat Window:** Full-screen chat interface
- **Settings Cards:** Grid-based settings layout

---

## 9. API Endpoints

### Authentication APIs:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/signup` | User registration |
| GET/POST | `/login` | User authentication |
| GET | `/logout` | Session termination |
| GET/POST | `/forgot-password` | Password recovery |
| GET/POST | `/reset-password` | Password reset |

### Flight APIs:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with search |
| GET | `/api/search_flights` | Search flights (JSON) |
| GET | `/results` | Display search results |

### Booking APIs:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/confirm_booking/<flight_id>` | Booking page |
| POST | `/book_flight/<flight_id>` | Process booking |
| GET | `/my_bookings` | User's bookings |

### User APIs:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/profile` | User profile |
| GET | `/settings` | Settings page |
| POST | `/change-password` | Update password |
| GET | `/delete-account` | Delete account |

### AI Assistant APIs:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ai-helper` | AI chat page |
| POST | `/assistant` | Process AI query |
| POST | `/api/calculate_price` | Calculate pricing |

---

## 10. Security Features

### Implemented Security Measures:

1. **Password Hashing:**
   - Using Werkzeug's `generate_password_hash()` and `check_password_hash()`
   - Passwords never stored in plain text

2. **Session Management:**
   - Flask secure sessions with secret key
   - Session-based authentication
   - Session cleared on logout

3. **Input Validation:**
   - Server-side validation for all forms
   - Minimum password length enforcement (6 characters)
   - Email format validation

4. **Protected Routes:**
   - Login required for booking, profile, settings
   - User-specific data access only

5. **CSRF Protection:**
   - Form-based submissions with method validation

6. **Error Handling:**
   - Graceful error messages
   - Invalid ID handling
   - Database error catching

---

## 11. Future Enhancements

### Planned Features:
1. **Payment Gateway Integration:** Stripe/PayPal for real payments
2. **Email Notifications:** Booking confirmations, flight reminders
3. **Seat Selection:** Choose specific seats on flight
4. **Meal Preferences:** Select in-flight meals
5. **Loyalty Program:** Points system for frequent flyers
6. **Flight Tracking:** Real-time flight status updates
7. **Mobile App:** Native iOS/Android applications
8. **Multi-language Support:** Urdu, Arabic, English
9. **Price Alerts:** Notify when prices drop
10. **Social Login:** Google, Facebook authentication

### Technical Improvements:
1. Add comprehensive unit tests
2. Implement caching for better performance
3. Add rate limiting for API endpoints
4. Implement proper email-based password reset
5. Add booking cancellation feature
6. Implement flight comparison feature

---

## 12. Conclusion

SkyVoyage is a comprehensive flight booking system that successfully addresses the challenges faced by traditional booking platforms. The application provides:

- **User-Friendly Interface:** Modern, intuitive design that works on all devices
- **Smart Features:** AI assistant, voice support, dynamic pricing
- **Secure Platform:** Hashed passwords, protected routes, input validation
- **Flexible Booking:** Support for multiple passengers, classes, and trip types
- **Promotional System:** Multiple discount codes and automatic infant discounts

The project demonstrates proficiency in:
- Full-stack web development with Python/Flask
- NoSQL database design with MongoDB
- Responsive frontend development
- RESTful API design
- User authentication and security
- AI chatbot implementation

---

## Project Statistics

| Metric | Count |
|--------|-------|
| Total Python Lines of Code | ~760 |
| Total HTML Templates | 13 |
| Database Collections | 4 |
| API Endpoints | 15+ |
| Responsive Breakpoints | 5 |
| Discount Codes | 6 |
| Supported Airlines | 5 |

---

## File Structure

```
flight_booking/
├── app.py                  # Main Flask application
├── seed_flights.py         # Database seeder script
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python runtime version
├── PROJECT_REPORT.md      # This report
├── templates/
│   ├── base.html          # Base template with navbar
│   ├── index.html         # Home page with search
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── profile.html       # User profile
│   ├── settings.html      # User settings
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── confirm_booking.html
│   ├── my_bookings.html
│   ├── results.html       # Search results
│   ├── search.html
│   └── ai_helper.html     # AI assistant page
└── venv/                  # Virtual environment
```

---

**Developed by:** Student  
**Institution:** Air University  
**Student ID:** 233757  
**Date:** December 2025

---

*This project report is auto-generated based on the actual codebase analysis.*


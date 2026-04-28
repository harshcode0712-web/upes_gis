"""
UPES Campus Explorer — Web-Based GIS Application
Covers: Bidholi (Energy Acres) & Kandoli (Knowledge Acres)
Categories: Academic Buildings, Sports Facilities, Cafes & Canteens
"""

from flask import Flask, jsonify, request, render_template
import math

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────
# UPES CAMPUS DATA
# Bidholi (Energy Acres): 30.4159, 77.9667
# Kandoli (Knowledge Acres): 30.3836, 77.9698
# ─────────────────────────────────────────────────────────────────────

PLACES = [

    # ════════════════════════════════════════
    # BIDHOLI CAMPUS — ACADEMIC BUILDINGS
    # ════════════════════════════════════════
    {
        "id": 1, "campus": "bidholi", "type": "academic",
        "name": "School of Computer Science (SCS)",
        "short": "SCS Block",
        "lat": 30.4165, "lng": 77.9672,
        "description": "Home to B.Tech CSE, MCA, M.Tech programs. Houses advanced computing labs, AI/ML lab, and cybersecurity lab.",
        "floors": "G+4", "capacity": "2000+ students", "hours": "8AM–8PM",
        "highlight": "AI & ML Research Lab"
    },
    {
        "id": 2, "campus": "bidholi", "type": "academic",
        "name": "School of Advanced Engineering (SAE)",
        "short": "SAE Block",
        "lat": 30.4168, "lng": 77.9660,
        "description": "Core engineering disciplines — Mechanical, Civil, Electrical, Petroleum Engineering. State-of-the-art workshop and simulation labs.",
        "floors": "G+3", "capacity": "1800+ students", "hours": "8AM–8PM",
        "highlight": "Petroleum Engineering Lab"
    },
    {
        "id": 3, "campus": "bidholi", "type": "academic",
        "name": "School of Health Sciences & Technology",
        "short": "Health Sciences Block",
        "lat": 30.4162, "lng": 77.9680,
        "description": "Pharmacy, Biotech, and Health Sciences programs. Equipped with pharmaceutical labs and medical simulation facilities.",
        "floors": "G+3", "capacity": "800+ students", "hours": "8AM–7PM",
        "highlight": "Pharmaceutical Lab"
    },
    {
        "id": 4, "campus": "bidholi", "type": "academic",
        "name": "School of Design (SOD)",
        "short": "Design Block",
        "lat": 30.4155, "lng": 77.9675,
        "description": "B.Des and M.Des programs in Communication, Product & Space Design. Features design studios and fabrication lab.",
        "floors": "G+2", "capacity": "500+ students", "hours": "9AM–7PM",
        "highlight": "Design Studio & Fab Lab"
    },
    {
        "id": 5, "campus": "bidholi", "type": "academic",
        "name": "Central Library — Bidholi",
        "short": "Main Library",
        "lat": 30.4158, "lng": 77.9665,
        "description": "6-floor central library with 1 lakh+ books, e-journals, digital resources, and silent study zones.",
        "floors": "G+5", "capacity": "500 seats", "hours": "8AM–10PM",
        "highlight": "1 Lakh+ Books & E-Journals"
    },
    {
        "id": 6, "campus": "bidholi", "type": "academic",
        "name": "Administrative Block — Bidholi",
        "short": "Admin Block",
        "lat": 30.4161, "lng": 77.9657,
        "description": "Main administrative hub — Registrar office, Admissions, Finance, and Student Affairs departments.",
        "floors": "G+2", "capacity": "—", "hours": "9AM–5:30PM",
        "highlight": "Registrar & Student Affairs"
    },
    {
        "id": 7, "campus": "bidholi", "type": "academic",
        "name": "Auditorium — Bidholi",
        "short": "Main Auditorium",
        "lat": 30.4170, "lng": 77.9668,
        "description": "1500-seat auditorium hosting convocations, cultural events, TEDx UPES, and inter-college competitions.",
        "floors": "G+1", "capacity": "1500 seats", "hours": "Event-based",
        "highlight": "TEDx UPES & Convocation Venue"
    },

    # ════════════════════════════════════════
    # BIDHOLI CAMPUS — SPORTS
    # ════════════════════════════════════════
    {
        "id": 8, "campus": "bidholi", "type": "sports",
        "name": "Cricket Ground — Bidholi",
        "short": "Cricket Ground",
        "lat": 30.4175, "lng": 77.9655,
        "description": "Full-size turf cricket ground used for inter-college tournaments and university championship matches.",
        "surface": "Natural turf", "capacity": "500 spectators", "hours": "6AM–8PM",
        "highlight": "Inter-college Tournaments"
    },
    {
        "id": 9, "campus": "bidholi", "type": "sports",
        "name": "Football Ground — Bidholi",
        "short": "Football Field",
        "lat": 30.4172, "lng": 77.9648,
        "description": "FIFA-standard football field for official matches and practice sessions.",
        "surface": "Natural grass", "capacity": "300 spectators", "hours": "6AM–8PM",
        "highlight": "University Football League"
    },
    {
        "id": 10, "campus": "bidholi", "type": "sports",
        "name": "Basketball Courts — Bidholi",
        "short": "Basketball Court",
        "lat": 30.4160, "lng": 77.9650,
        "description": "Two outdoor basketball courts with floodlights for evening play.",
        "surface": "Concrete", "capacity": "—", "hours": "6AM–9PM",
        "highlight": "Floodlit Evening Courts"
    },
    {
        "id": 11, "campus": "bidholi", "type": "sports",
        "name": "Badminton Hall — Bidholi",
        "short": "Indoor Badminton",
        "lat": 30.4163, "lng": 77.9645,
        "description": "4-court indoor badminton hall with wooden flooring and professional lighting.",
        "surface": "Wooden floor", "capacity": "4 courts", "hours": "6AM–9PM",
        "highlight": "Professional Indoor Courts"
    },
    {
        "id": 12, "campus": "bidholi", "type": "sports",
        "name": "Gym & Fitness Centre — Bidholi",
        "short": "Fitness Centre",
        "lat": 30.4157, "lng": 77.9658,
        "description": "Fully equipped gym with cardio machines, free weights, and certified personal trainers.",
        "surface": "Indoor", "capacity": "100 persons", "hours": "5:30AM–9PM",
        "highlight": "Certified Personal Trainers"
    },
    {
        "id": 13, "campus": "bidholi", "type": "sports",
        "name": "Swimming Pool — Bidholi",
        "short": "Swimming Pool",
        "lat": 30.4153, "lng": 77.9660,
        "description": "Olympic-size swimming pool with separate lanes for competitive and recreational swimming.",
        "surface": "Olympic pool", "capacity": "8 lanes", "hours": "6AM–8PM",
        "highlight": "Olympic-size Pool"
    },
    {
        "id": 14, "campus": "bidholi", "type": "sports",
        "name": "Tennis Courts — Bidholi",
        "short": "Tennis Courts",
        "lat": 30.4166, "lng": 77.9643,
        "description": "Two synthetic tennis courts with floodlights and ball machine facility.",
        "surface": "Synthetic", "capacity": "2 courts", "hours": "6AM–9PM",
        "highlight": "Ball Machine Facility"
    },

    # ════════════════════════════════════════
    # BIDHOLI CAMPUS — CAFES & CANTEENS
    # ════════════════════════════════════════
    {
        "id": 15, "campus": "bidholi", "type": "cafe",
        "name": "Main Cafeteria — Bidholi",
        "short": "Main Caf",
        "lat": 30.4159, "lng": 77.9670,
        "description": "Largest dining facility on campus. Serves North Indian, South Indian, Chinese and Continental cuisines.",
        "seating": "600 seats", "hours": "7AM–10PM",
        "speciality": "Full meals, thali, live counters",
        "highlight": "Multi-cuisine, 600 seats"
    },
    {
        "id": 16, "campus": "bidholi", "type": "cafe",
        "name": "Café Coffee Day — Bidholi",
        "short": "CCD Bidholi",
        "lat": 30.4164, "lng": 77.9674,
        "description": "Official CCD outlet on campus serving premium coffee, cold beverages, sandwiches and snacks.",
        "seating": "50 seats", "hours": "8AM–9PM",
        "speciality": "Cold coffee, frappuccino, snacks",
        "highlight": "Premium Coffee & Quick Bites"
    },
    {
        "id": 17, "campus": "bidholi", "type": "cafe",
        "name": "SCS Block Canteen",
        "short": "SCS Canteen",
        "lat": 30.4167, "lng": 77.9669,
        "description": "Quick service canteen inside the SCS block. Popular for momos, maggi, sandwiches and tea.",
        "seating": "80 seats", "hours": "8AM–8PM",
        "speciality": "Momos, Maggi, Tea & Coffee",
        "highlight": "Student Favourite — Momos!"
    },
    {
        "id": 18, "campus": "bidholi", "type": "cafe",
        "name": "Engineering Block Dhaba",
        "short": "Engg Dhaba",
        "lat": 30.4169, "lng": 77.9658,
        "description": "Casual outdoor dhaba-style canteen near SAE block. Famous for chai, samosas and lunch combos.",
        "seating": "120 seats", "hours": "7:30AM–7PM",
        "speciality": "Chai, Samosa, Lunch Thali",
        "highlight": "Best chai on campus!"
    },
    {
        "id": 19, "campus": "bidholi", "type": "cafe",
        "name": "Hostel Food Court — Bidholi",
        "short": "Hostel Food Court",
        "lat": 30.4150, "lng": 77.9663,
        "description": "Evening food court near hostels. Open late with fast food, juice bar, and street-food stalls.",
        "seating": "200 seats", "hours": "4PM–11PM",
        "speciality": "Fast food, juices, street food",
        "highlight": "Open till 11 PM"
    },

    # ════════════════════════════════════════
    # KANDOLI CAMPUS — ACADEMIC BUILDINGS
    # ════════════════════════════════════════
    {
        "id": 20, "campus": "kandoli", "type": "academic",
        "name": "School of Business (SOB)",
        "short": "Business Block",
        "lat": 30.3840, "lng": 77.9702,
        "description": "MBA, BBA, and Management programs. Features Bloomberg Terminal lab, stock trading simulation room.",
        "floors": "G+4", "capacity": "1500+ students", "hours": "8AM–8PM",
        "highlight": "Bloomberg Terminal Lab"
    },
    {
        "id": 21, "campus": "kandoli", "type": "academic",
        "name": "School of Law (SOL)",
        "short": "Law Block",
        "lat": 30.3843, "lng": 77.9692,
        "description": "BBA-LLB, BA-LLB, and LLM programs. Includes moot court, legal aid clinic, and law library.",
        "floors": "G+3", "capacity": "800+ students", "hours": "8AM–8PM",
        "highlight": "Moot Court & Legal Aid Clinic"
    },
    {
        "id": 22, "campus": "kandoli", "type": "academic",
        "name": "School of Liberal Studies (SLS)",
        "short": "Liberal Studies Block",
        "lat": 30.3837, "lng": 77.9705,
        "description": "BA programs in Psychology, Economics, Journalism, and Humanities. Features debate hall and media lab.",
        "floors": "G+3", "capacity": "700+ students", "hours": "8AM–7PM",
        "highlight": "Media Lab & Debate Hall"
    },
    {
        "id": 23, "campus": "kandoli", "type": "academic",
        "name": "School of Modern Media (SMM)",
        "short": "Media Block",
        "lat": 30.3834, "lng": 77.9698,
        "description": "Mass Communication, Journalism, and Film programs. Equipped with broadcast studio, edit suites, and green screen room.",
        "floors": "G+2", "capacity": "400+ students", "hours": "8AM–7PM",
        "highlight": "Broadcast Studio & Edit Suites"
    },
    {
        "id": 24, "campus": "kandoli", "type": "academic",
        "name": "Central Library — Kandoli",
        "short": "Kandoli Library",
        "lat": 30.3838, "lng": 77.9695,
        "description": "Well-stocked library with law journals, business case studies, and digital resource access.",
        "floors": "G+3", "capacity": "300 seats", "hours": "8AM–10PM",
        "highlight": "Law Journals & Case Studies"
    },
    {
        "id": 25, "campus": "kandoli", "type": "academic",
        "name": "Administrative Block — Kandoli",
        "short": "Admin Block",
        "lat": 30.3836, "lng": 77.9701,
        "description": "Campus administration, Dean's office, Examination cell, and Student Welfare office.",
        "floors": "G+2", "capacity": "—", "hours": "9AM–5:30PM",
        "highlight": "Dean's Office & Exam Cell"
    },
    {
        "id": 26, "campus": "kandoli", "type": "academic",
        "name": "Seminar Hall & Auditorium — Kandoli",
        "short": "Kandoli Auditorium",
        "lat": 30.3845, "lng": 77.9700,
        "description": "800-seat auditorium used for academic seminars, cultural programs, and guest lectures.",
        "floors": "G+1", "capacity": "800 seats", "hours": "Event-based",
        "highlight": "Guest Lectures & Cultural Events"
    },

    # ════════════════════════════════════════
    # KANDOLI CAMPUS — SPORTS
    # ════════════════════════════════════════
    {
        "id": 27, "campus": "kandoli", "type": "sports",
        "name": "Cricket Ground — Kandoli",
        "short": "Cricket Ground",
        "lat": 30.3847, "lng": 77.9690,
        "description": "Well-maintained cricket ground with practice nets and a pavilion for players.",
        "surface": "Natural turf", "capacity": "300 spectators", "hours": "6AM–8PM",
        "highlight": "Practice Nets & Pavilion"
    },
    {
        "id": 28, "campus": "kandoli", "type": "sports",
        "name": "Basketball Courts — Kandoli",
        "short": "Basketball Court",
        "lat": 30.3833, "lng": 77.9703,
        "description": "Two outdoor basketball courts with line markings and floodlights.",
        "surface": "Concrete", "capacity": "—", "hours": "6AM–9PM",
        "highlight": "Floodlit Courts"
    },
    {
        "id": 29, "campus": "kandoli", "type": "sports",
        "name": "Badminton & Table Tennis Hall — Kandoli",
        "short": "Indoor Sports Hall",
        "lat": 30.3835, "lng": 77.9708,
        "description": "Indoor hall with 2 badminton courts and 4 table tennis tables.",
        "surface": "Wooden floor", "capacity": "2 badminton + 4 TT", "hours": "6AM–9PM",
        "highlight": "Badminton + Table Tennis"
    },
    {
        "id": 30, "campus": "kandoli", "type": "sports",
        "name": "Gym — Kandoli",
        "short": "Kandoli Gym",
        "lat": 30.3841, "lng": 77.9707,
        "description": "Well-equipped gym facility for hostel students with cardio and strength training equipment.",
        "surface": "Indoor", "capacity": "60 persons", "hours": "5:30AM–9PM",
        "highlight": "Open for Hostel Students"
    },
    {
        "id": 31, "campus": "kandoli", "type": "sports",
        "name": "Volleyball & Futsal Court — Kandoli",
        "short": "Volleyball / Futsal",
        "lat": 30.3829, "lng": 77.9696,
        "description": "Multi-use outdoor court for volleyball and futsal games.",
        "surface": "Concrete", "capacity": "—", "hours": "6AM–8PM",
        "highlight": "Multi-sport Outdoor Court"
    },

    # ════════════════════════════════════════
    # KANDOLI CAMPUS — CAFES & CANTEENS
    # ════════════════════════════════════════
    {
        "id": 32, "campus": "kandoli", "type": "cafe",
        "name": "Main Cafeteria — Kandoli",
        "short": "Main Caf Kandoli",
        "lat": 30.3839, "lng": 77.9699,
        "description": "Main dining facility at Kandoli campus with hot meals, snacks, and beverages throughout the day.",
        "seating": "400 seats", "hours": "7AM–10PM",
        "speciality": "Indian meals, snacks, beverages",
        "highlight": "400-seat Main Dining Hall"
    },
    {
        "id": 33, "campus": "kandoli", "type": "cafe",
        "name": "Café Coffee Day — Kandoli",
        "short": "CCD Kandoli",
        "lat": 30.3842, "lng": 77.9694,
        "description": "CCD outlet near the SOB block. Popular for coffee and snacks between classes.",
        "seating": "40 seats", "hours": "8AM–9PM",
        "speciality": "Espresso, cold coffee, wraps",
        "highlight": "Between-class Coffee Stop"
    },
    {
        "id": 34, "campus": "kandoli", "type": "cafe",
        "name": "Law Block Canteen",
        "short": "Law Canteen",
        "lat": 30.3844, "lng": 77.9690,
        "description": "Quick bites canteen inside the law block. Popular for sandwiches, tea, and quick snacks.",
        "seating": "60 seats", "hours": "8AM–7PM",
        "speciality": "Sandwiches, chai, quick snacks",
        "highlight": "Law Students' Favourite Spot"
    },
    {
        "id": 35, "campus": "kandoli", "type": "cafe",
        "name": "Hostel Food Court — Kandoli",
        "short": "Hostel Food Court",
        "lat": 30.3831, "lng": 77.9704,
        "description": "Evening food court near student hostels with street food stalls, juice bar, and snacks.",
        "seating": "150 seats", "hours": "4PM–11PM",
        "speciality": "Street food, juice bar, snacks",
        "highlight": "Evening Hangout Spot"
    },
]

# Category & campus info
CAMPUS_INFO = {
    "bidholi": {
        "name": "Energy Acres — Bidholi",
        "lat": 30.4159, "lng": 77.9667,
        "schools": ["SCS", "SAE", "Health Sciences", "Design"],
        "tagline": "Engineering, Technology & Sciences"
    },
    "kandoli": {
        "name": "Knowledge Acres — Kandoli",
        "lat": 30.3836, "lng": 77.9698,
        "schools": ["Business", "Law", "Liberal Studies", "Modern Media"],
        "tagline": "Management, Law & Humanities"
    }
}

# ─────────────────────────────────────────────────────────────────────
# SPATIAL UTILITIES
# ─────────────────────────────────────────────────────────────────────

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def nearest_neighbors(lat, lng, ptype=None, campus=None, k=5):
    candidates = PLACES
    if ptype:
        candidates = [p for p in candidates if p["type"] == ptype]
    if campus:
        candidates = [p for p in candidates if p["campus"] == campus]
    scored = [{**p, "distance_m": round(haversine(lat, lng, p["lat"], p["lng"]) * 1000, 0)} for p in candidates]
    scored.sort(key=lambda x: x["distance_m"])
    return scored[:k]


def search_places(query, ptype=None, campus=None):
    query = query.lower().strip()
    results = []
    for p in PLACES:
        if ptype and p["type"] != ptype:
            continue
        if campus and p["campus"] != campus:
            continue
        text = f"{p['name']} {p['short']} {p['description']} {p['campus']} {p['type']}".lower()
        if query in text:
            results.append(p)
    return results


# ─────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("upes.html")

@app.route("/api/places")
def get_places():
    ptype = request.args.get("type")
    campus = request.args.get("campus")
    data = PLACES
    if ptype:
        data = [p for p in data if p["type"] == ptype]
    if campus:
        data = [p for p in data if p["campus"] == campus]
    return jsonify({"places": data, "count": len(data)})

@app.route("/api/search")
def search():
    q = request.args.get("q", "").strip()
    ptype = request.args.get("type")
    campus = request.args.get("campus")
    if not q:
        return jsonify({"results": [], "query": q})
    results = search_places(q, ptype, campus)
    return jsonify({"results": results, "query": q, "count": len(results)})

@app.route("/api/nearest")
def nearest():
    try:
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))
        k = int(request.args.get("k", 5))
        ptype = request.args.get("type") or None
        campus = request.args.get("campus") or None
        results = nearest_neighbors(lat, lng, ptype, campus, k)
        return jsonify({"results": results, "query_lat": lat, "query_lng": lng})
    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/stats")
def stats():
    from collections import Counter
    types = Counter(p["type"] for p in PLACES)
    campuses = Counter(p["campus"] for p in PLACES)
    return jsonify({
        "total": len(PLACES),
        "by_type": dict(types),
        "by_campus": dict(campuses),
        "campus_info": CAMPUS_INFO,
    })

if __name__ == "__main__":
    print("=" * 55)
    print("  UPES Campus Explorer GIS")
    print("  Open http://127.0.0.1:5000 in your browser")
    print("=" * 55)
    app.run(debug=True)
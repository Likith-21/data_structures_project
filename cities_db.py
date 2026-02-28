"""Indian cities database for autocomplete suggestions."""

MAJOR_INDIAN_CITIES = [
    # Metros
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    
    # Major Cities
    "Indore", "Chandigarh", "Kochi", "Patna", "Vadodara",
    "Srinagar", "Bhopal", "Nagpur", "Coimbatore", "Chandigarh",
    "Mysore", "Visakhapatnam", "Guwahati", "Kota", "Rajkot",
    "Surat", "Agra", "Varanasi", "Allahabad", "Kanpur",
    
    # Tamil Nadu
    "Chennai", "Coimbatore", "Madurai", "Salem", "Tiruppur",
    "Chittoor", "Chittoor City", "Tirupati", "Vellore", "Nagarcoil",
    "Kanyakumari", "Thanjavur", "Trichy", "Erode",
    
    # Andhra Pradesh
    "Hyderabad", "Visakhapatnam", "Vijayawada", "Guntur", "Tirupati",
    "Nellore", "Rajahmundry", "Warangal", "Kurnool",
    
    # Karnataka
    "Bangalore", "Bangalore City", "Mysore", "Mangalore", "Hubli",
    "Belgaum", "Shimoga", "Gulbarga", "Bijapur", "Udupi",
    
    # Maharashtra
    "Mumbai", "Pune", "Nagpur", "Aurangabad", "Nashik",
    "Solapur", "Akola", "Kolhapur", "Amravati", "Thane",
    
    # Uttar Pradesh
    "Delhi", "Lucknow", "Kanpur", "Varanasi", "Agra",
    "Allahabad", "Ghaziabad", "Meerut", "Noida", "Bareilly",
    
    # Rajasthan
    "Jaipur", "Jodhpur", "Udaipur", "Bikaner", "Kota",
    "Ajmer", "Pushkar", "Mount Abu", "Jaisalmer",
    
    # Gujarat
    "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar",
    "Gandhinagar", "Porbandar", "Junagadh", "Anand",
    
    # West Bengal
    "Kolkata", "Darjeeling", "Siliguri", "Asansol", "Durgapur",
    "Kharagpur", "Hastings",
    
    # Punjab
    "Chandigarh", "Amritsar", "Ludhiana", "Jalandhar", "Patiala",
    "Bathinda", "Moga", "Sangrur",
    
    # Himachal Pradesh
    "Shimla", "Manali", "Kasol", "Dharamshala", "Kullu",
    "Solan", "Mandi", "Kangra",
    
    # Uttarakhand
    "Dehradun", "Nainital", "Mussoorie", "Rishikesh", "Haridwar",
    "Shimla", "Srinagar", "Almora",
    
    # Kerala
    "Kochi", "Thiruvananthapuram", "Kottayam", "Ernakulam", "Kannur",
    "Kozhikode", "Thrissur", "Alappuzha", "Kasaragod",
    
    # Telangana
    "Hyderabad", "Warangal", "Nizamabad", "Khammam", "Karimnagar",
    
    # Goa
    "Panaji", "Margao", "Vasco", "Ponda", "Pernem",
    
    # Assam
    "Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Tezpur",
    
    # Bihar
    "Patna", "Gaya", "Muzaffarpur", "Darbhanga", "Purnia",
    "Bhagalpur", "Arrah", "Bihar Sharif",
    
    # Jharkhand
    "Ranchi", "Jamshedpur", "Dhanbad", "Giridih", "Bokaro",
    "Hazaribagh", "Dumka", "Deoghar",
    
    # Odisha
    "Bhubaneswar", "Cuttack", "Rourkela", "Balasore", "Sambalpur",
    "Puri", "Berhampur", "Bargarh",
    
    # Madhya Pradesh
    "Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain",
    "Sagar", "Ratlam", "Katni", "Chhindwara",
]


def get_city_suggestions(search_text: str, limit: int = 10) -> list:
    """Get city suggestions based on search text."""
    if not search_text:
        return MAJOR_INDIAN_CITIES[:limit]
    
    search_lower = search_text.lower()
    matches = [city for city in MAJOR_INDIAN_CITIES if city.lower().startswith(search_lower)]
    
    # If no prefix matches, try substring matches
    if not matches:
        matches = [city for city in MAJOR_INDIAN_CITIES if search_lower in city.lower()]
    
    return matches[:limit]

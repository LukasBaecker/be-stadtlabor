from geopy.geocoders import Nominatim

def geocoder(address):
    geolocator = Nominatim(user_agent="gardens")
    location = geolocator.geocode(address)
    return [location.latitude, location.longitude]
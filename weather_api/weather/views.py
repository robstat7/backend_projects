from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import WeatherSerializer
from .cache import get_cache, set_cache

API_KEY = "<your-openweathermap.org-api-key>"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@api_view(['GET'])
def get_weather(request):
	city = request.query_params.get('city')
	
	if not city:
	    return Response({"error": "City parameter is required"},\
	    		status=status.HTTP_400_BAD_REQUEST)
	
	# Check Redis cache
	cache_key = f"weather:{city.lower()}"
	cached_data = get_cache(cache_key)
	if cached_data:
	    return Response({"data": cached_data, "source": "cache"},\
			    status=status.HTTP_200_OK)
	
	# Fetch data from OpenWeatherMap API
	params = {
	    "q": city,
	    "appid": API_KEY,
	    "units": "metric"
	}
	response = requests.get(BASE_URL, params=params)
	
	if response.status_code == 200:
		data = response.json()
		simplified_data = {
		    "city": data["name"],
		    "temperature": data["main"]["temp"],
		    "description": data["weather"][0]["description"]
		}
		
		# Cache the data in Redis for 1 hour
		set_cache(cache_key, simplified_data, expiry=3600)
		return Response({"data": simplified_data, "source": "api"},\
				status=status.HTTP_200_OK)
	else:
		return Response({"error": response.json().get("message", "Unable to \
			 fetch weather data.")},\
			status=response.status_code)

import googlemaps
from django.http import JsonResponse

def reverse_coordinates_to_address(latitude, longitude):
        gmaps = googlemaps.Client(key='AIzaSyByDKQqYXSuGl9tBZ9rj341jBW_enAVMlg')
        results = gmaps.reverse_geocode((latitude, longitude))
        return JsonResponse({'results':results})

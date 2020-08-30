from mapbox import Geocoder

geocoder = Geocoder(access_token="pk.eyJ1IjoiZmFsdHVmYWx0dW1hc3QiLCJhIjoiY2pzZmtrMWdlMWZjYTQzbG5yMHllM2QzMCJ9.As3_2UKt_dWFBS7bS1SiGw")

def get_coordinates(address):
	response = geocoder.forward(address)
	try: return response.json()['features'][0]['geometry']['coordinates']
	except IndexError: return [None, None]

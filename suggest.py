from flask import Blueprint, request, jsonify
import requests


suggest_bp = Blueprint('suggest', __name__)


def execute_query(query):
    from app import connection2
    cursor = connection2.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result


@suggest_bp.route('/getType', methods=['GET'])
def get_travel_type():
    try:
        from app import connection2

        cursor = connection2.cursor()

        select_query = "SELECT * FROM saveSuggest"
        cursor.execute(select_query)

        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result

    except Exception as e:
        # Handle the exception appropriately, e.g., log the error or return an error response
        print(f"An error occurred: {str(e)}")
        return "Error: Failed to retrieve travel types"




@suggest_bp.route('/restplaces', methods=['GET'])
def get_travel_places():
    print("methana")

    
    tags = '[tourism=hotel]'
    
    filtered_places = fetch_filtered_traveling_places(tags)


    return(filtered_places)



@suggest_bp.route('/agentplaces', methods=['GET'])
def get_travel_placesAgent():
    print("methana")

    tags = '[tourism=viewpoint]'
    
    filtered_places = fetch_filtered_traveling_places(tags)


    return(filtered_places)



@suggest_bp.route('/sportplaces', methods=['GET'])
def get_travel_placesSport():
    print("methana")

    tags = '[tourism=museum]'
    
    filtered_places = fetch_filtered_traveling_places(tags)


    return(filtered_places)



@suggest_bp.route('/spaplaces', methods=['GET'])
def get_travel_placesSpa():

    tags = '[tourism=artwork]'
    
    filtered_places = fetch_filtered_traveling_places(tags)


    return(filtered_places)



@suggest_bp.route('/allplaces', methods=['GET'])
def get_Alltravel_places():
    try:
        location = execute_query("SELECT * FROM saveSuggest")
        
        print(location)
        # Perform location filtering using OpenStreetMap Nominatim service
        filtered_results = filter_location(location)

        # Return the filtered results as JSON response
        return jsonify(filtered_results)

    except Exception as e:
        # Handle the exception appropriately, e.g., log the error or return an error response
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "Failed to retrieve travel places"})


    


def filter_location(location):
    one , two = location

    print(one)
    print(two)
    base_url = 'https://nominatim.openstreetmap.org/search'
    # params = {'q': location, 'format': 'json', 'limit': 10,'countrycodes':'LK'}
    params = {'format': 'json', 'limit': 10, 'countrycodes': 'LK', 'type': two}
    del params['limit']
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        filtered_results = []
        for result in data:
            
            place = {
                'Name': result.get('display_name'),
                'latitude': result.get('lat'),
                'longitude': result.get('lon'),
                'Type': result.get('type'),
                'Class': result.get('class')
            }
            filtered_results.append(place)

        
    params = {'q': one, 'format': 'json', 'limit': 10, 'countrycodes': 'LK'}

    del params['limit']
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        filtered_results = []
        for result in data:
            
            place = {
                'Name': result.get('display_name'),
                'latitude': result.get('lat'),
                'longitude': result.get('lon'),
                'Type': result.get('type'),
                'Class': result.get('class')
            }
            filtered_results.append(place)
        
    return filtered_results
    



def fetch_filtered_traveling_places(tags):
    # Construct the API URL with necessary parameters and filters
    api_url = 'https://www.overpass-api.de/api/interpreter'
    query = '[out:json];' \
            'area[name="Sri Lanka"];' \
            'node(area)' + tags + ';' \
            'out center;'
    
    
    # Send an HTTP GET request to the API URL with the query
    response = requests.get(api_url, params={'data': query})
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        filtered_results = []
        print(data['elements'])
        for result in data['elements']:
            tags_list = result.get('tags')
            
            place = {
                'Name': tags_list.get('name'),
                'latitude': result.get('lat'),
                'longitude': result.get('lon'),
                'Type': tags_list.get('is_in'),
                'Class': tags_list.get('tourism')
            }
            filtered_results.append(place)
        
        # Extract the relevant information from the response
        # For example, you can access the list of places using 'data['elements']'
        
        # Return the filtered traveling places data
        return filtered_results
    
    # Return an empty list if there was an error or no data found
    return []


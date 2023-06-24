from flask import Blueprint, request
import json

# Create a Blueprint instance for the routes
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        print("Username:", username)
        print("Password:", password)

        from app import connection2
        cursor = connection2.cursor()

        query = "SELECT * FROM login WHERE name = %s AND password = %s"
        values = (username, password)

        cursor.execute(query, values)

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # Authentication successful
            # Perform the desired actions, such as granting access or redirecting to another page
            return json.dumps("Authentication successful")
        else:
            # Authentication failed
            # Perform the desired actions, such as displaying an error message or redirecting to a login page
            return json.dumps("Authentication failed")

    except Exception as e:
        # Handle the exception appropriately, e.g., log the error or return an error response
        print(f"An error occurred: {str(e)}")
        return json.dumps({"error": "Failed to authenticate"})

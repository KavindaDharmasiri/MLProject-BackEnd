from flask import Blueprint, request
import mysql.connector as connection
db = connection.connect(host='database-midway.cnjonpzevrxo.us-east-1.rds.amazonaws.com',user='admin', password='root1234', database= 'midway')

# Create a Blueprint instance for the routes
signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST'])
def signup():
    try:
        mycursor = db.cursor()

        qury = 'CREATE TABLE IF NOT EXISTS login (name VARCHAR(50), email VARCHAR(50), password VARCHAR(50))'
        mycursor.execute(qury)

        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')

        print("Username:", name)
        print("Email:", email)
        print("Password:", password)

        qury = 'INSERT INTO login (name, email, password) VALUES (%s, %s, %s)'
        value = (name, email, password)
        mycursor.execute(qury, value)

        db.commit()

        mycursor.close()
        db.close()

        return 'Signup successful'

    except Exception as e:
        # Handle the exception appropriately, e.g., log the error or return an error response
        print(f"An error occurred: {str(e)}")
        return "error Failed to signup"

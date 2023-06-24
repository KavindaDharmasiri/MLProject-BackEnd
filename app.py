from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from login import login_bp
from signup import signup_bp
from suggest import suggest_bp
from search import search_bp
import mysql.connector as connection

    
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "hello"


def create_connection():
    # Establish the database connection
    connection1 = connection.connect(host='database-midway.cnjonpzevrxo.us-east-1.rds.amazonaws.com',user='admin', password='root1234', database= 'midway')

    return connection1

connection2 = create_connection()


app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(suggest_bp)
app.register_blueprint(search_bp)



# db = connection.connect(host='database-midway.cnjonpzevrxo.us-east-1.rds.amazonaws.com',user='admin', password='root1234', database='database-midway')

#     mycursor = db.cursor()
#     qury = 'insert into customer(name,address,salary) value ("sirimal","Galle","1000")'

#     mycursor.execute(qury)

#     db.commit()
#     print(mycursor.rowcount, "record inserted.")


def makeConnection(self):
    db = connection.connect(host='database-midway.cnjonpzevrxo.us-east-1.rds.amazonaws.com',user='admin', password='root1234', database='database-midway')

    mycursor = db.cursor()
    qury = 'create table if not exists customer(name varchar(50),address varchar(50),salary varchar(50))'
    mycursor.execute(qury)

    return db






if __name__ == '__main__':
    app.run(debug=True)

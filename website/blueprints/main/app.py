from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")  # Update this in your .env file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Routes (Admin, Loans, Contracts, Auctions)
@app.route('/api/admin', methods=['GET'])
def admin():
    return jsonify({"message": "Admin route"})

@app.route('/api/loans', methods=['GET'])
def loans():
    return jsonify({"message": "Loans route"})

@app.route('/api/contracts', methods=['GET'])
def contracts():
    return jsonify({"message": "Contracts route"})

@app.route('/api/auctions', methods=['GET'])
def auctions():
    return jsonify({"message": "Auctions route"})

# Start server
if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))

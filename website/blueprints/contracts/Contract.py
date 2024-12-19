from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Update with your actual DB URI
db = SQLAlchemy(app)

# Define the Contract model
class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True, index=True)
    contract_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    posted_by = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='open')  # default status
    player_id = db.Column(db.Integer, nullable=True)  # Optional player ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Contract(id={self.id}, contract_id='{self.contract_id}', title='{self.title}', status='{self.status}')>"

# Sample code to create tables
with app.app_context():
    db.create_all()

# Example of adding a new contract (from Flask route)
@app.route("/contracts", methods=["POST"])
def add_contract():
    try:
        data = request.get_json()
        contract_id = data['contract_id']
        title = data['title']
        description = data['description']
        posted_by = data['posted_by']

        contract = Contract(contract_id=contract_id, title=title, description=description, posted_by=posted_by)
        db.session.add(contract)
        db.session.commit()

        return jsonify({
            'contract_id': contract.contract_id,
            'title': contract.title,
            'description': contract.description,
            'posted_by': contract.posted_by,
            'status': contract.status
        }), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Contract  # Assuming Contract model is defined in models.py
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Update with your actual DB URI
db = SQLAlchemy(app)

# Update contract status and assign player
@app.route("/contracts/<contract_id>", methods=["PUT"])
def update_contract(contract_id):
    try:
        # Retrieve the contract from the database using the contract_id
        contract = Contract.query.filter_by(contract_id=contract_id).first()

        if not contract:
            return jsonify({"message": "Contract not found"}), 404

        # Get updated values from the request body
        data = request.get_json()
        status = data.get("status")
        player_id = data.get("player_id")

        # Update contract fields
        if status:
            contract.status = status
        if player_id:
            contract.player_id = player_id

        # Commit changes to the database
        db.session.commit()

        # Return the updated contract details as a response
        return jsonify({
            'contract_id': contract.contract_id,
            'title': contract.title,
            'description': contract.description,
            'posted_by': contract.posted_by,
            'status': contract.status,
            'player_id': contract.player_id
        })

    except Exception as err:
        return jsonify({"error": str(err)}), 500


if __name__ == "__main__":
    app.run(debug=True)

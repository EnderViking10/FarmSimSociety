from flask import Blueprint, request, jsonify
from models import Loan, db

loan_bp = Blueprint("loan", __name__, url_prefix="/loan")

# Get loans by playerID
@loan_bp.route("/<player_id>", methods=["GET"])
def get_loan(player_id):
    try:
        loan = Loan.query.filter_by(player_id=player_id).first()
        if not loan:
            return jsonify({"message": "Loan not found"}), 404
        return jsonify(loan.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update or create loan for a player
@loan_bp.route("/", methods=["POST"])
def update_or_create_loan():
    data = request.json
    player_id = data.get("playerID")
    loan_amount = data.get("loanAmount")

    try:
        loan = Loan.query.filter_by(player_id=player_id).first()

        if loan:
            loan.loan_amount = loan_amount
            loan.last_updated = db.func.now()
            db.session.commit()
        else:
            loan = Loan(player_id=player_id, loan_amount=loan_amount)
            db.session.add(loan)
            db.session.commit()

        return jsonify(loan.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

const mongoose = require("mongoose");

const LoanSchema = new mongoose.Schema({
  playerID: { type: String, required: true },
  loanAmount: { type: Number, required: true },
  lastUpdated: { type: Date, default: Date.now },
});

module.exports = mongoose.model("Loan", LoanSchema);

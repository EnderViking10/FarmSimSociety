const express = require("express");
const router = express.Router();
const Loan = require("../models/Loan");

// Get loans by playerID
router.get("/:playerID", async (req, res) => {
  try {
    const loan = await Loan.findOne({ playerID: req.params.playerID });
    if (!loan) return res.status(404).json({ message: "Loan not found" });
    res.json(loan);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Update or create loan for a player
router.post("/", async (req, res) => {
  const { playerID, loanAmount } = req.body;
  try {
    let loan = await Loan.findOne({ playerID });
    if (loan) {
      loan.loanAmount = loanAmount;
      loan.lastUpdated = Date.now();
      await loan.save();
    } else {
      loan = new Loan({ playerID, loanAmount });
      await loan.save();
    }
    res.json(loan);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;

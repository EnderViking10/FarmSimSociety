const express = require("express");
const router = express.Router();
const Contract = require("../models/Contract");

// Get all contracts
router.get("/", async (req, res) => {
  try {
    const contracts = await Contract.find();
    res.json(contracts);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Add a new contract
router.post("/", async (req, res) => {
  const { contractID, title, description, postedBy } = req.body;
  try {
    const contract = new Contract({
      contractID,
      title,
      description,
      postedBy,
    });
    await contract.save();
    res.status(201).json(contract);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Update contract status
router.put("/:contractID", async (req, res) => {
  const { status, playerID } = req.body;
  try {
    const contract = await Contract.findOne({ contractID: req.params.contractID });
    if (!contract) return res.status(404).json({ message: "Contract not found" });

    contract.status = status;
    if (playerID) contract.playerID = playerID;
    await contract.save();

    res.json(contract);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;

const express = require("express");
const router = express.Router();
const Admin = require("../models/Admin");
const Log = require("../models/Log");
const { authenticate } = require("../middleware/auth");

// Admin Login
router.post("/login", async (req, res) => {
  const { username, password } = req.body;

  try {
    const admin = await Admin.findOne({ username });

    if (!admin || admin.password !== password) {
      return res.status(401).json({ message: "Invalid credentials" });
    }

    // Generate a simple session token (replace with JWT for production)
    const token = `token-${admin._id}-${Date.now()}`;
    res.json({ message: "Login successful", token });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Ban User
router.post("/ban", authenticate, async (req, res) => {
  const { playerID } = req.body;

  try {
    // Placeholder logic for banning a player
    // Actual implementation depends on the in-game player database
    console.log(`Player ${playerID} banned by admin.`);
    await Log.create({ action: "Ban Player", adminID: req.admin._id, details: { playerID } });
    res.json({ message: `Player ${playerID} banned successfully` });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// View All Auctions
router.get("/auctions", authenticate, async (req, res) => {
  try {
    const auctions = await Auction.find(); // Ensure Auction model is imported
    res.json(auctions);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Delete Auction
router.delete("/auction/:id", authenticate, async (req, res) => {
  const { id } = req.params;

  try {
    await Auction.findByIdAndDelete(id);
    await Log.create({ action: "Delete Auction", adminID: req.admin._id, details: { auctionID: id } });
    res.json({ message: "Auction deleted successfully" });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// View Logs
router.get("/logs", authenticate, async (req, res) => {
  try {
    const logs = await Log.find().populate("adminID", "username");
    res.json(logs);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;

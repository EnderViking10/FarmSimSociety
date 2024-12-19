const express = require("express");
const router = express.Router();
const Auction = require("../models/Auction");
const Bid = require("../models/Bid");

// Create New Auction
router.post("/create", async (req, res) => {
  const { itemID, itemName, sellerID, startingPrice, duration } = req.body;

  try {
    const endTime = new Date(Date.now() + duration * 60 * 1000); // Duration in minutes

    const auction = new Auction({
      itemID,
      itemName,
      sellerID,
      startingPrice,
      currentBid: startingPrice,
      endTime,
    });

    await auction.save();
    res.json({ message: "Auction created successfully", auction });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Place a Bid
router.post("/bid", async (req, res) => {
  const { auctionID, bidderID, amount } = req.body;

  try {
    const auction = await Auction.findById(auctionID);

    if (!auction || auction.status !== "active") {
      return res.status(404).json({ message: "Auction not found or already completed" });
    }

    if (amount <= auction.currentBid) {
      return res.status(400).json({ message: "Bid must be higher than the current bid" });
    }

    // Update auction with new bid
    auction.currentBid = amount;
    auction.currentBidderID = bidderID;
    await auction.save();

    // Log the bid
    const bid = new Bid({ auctionID, bidderID, amount });
    await bid.save();

    res.json({ message: "Bid placed successfully", auction });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get Active Auctions
router.get("/active", async (req, res) => {
  try {
    const activeAuctions = await Auction.find({ status: "active" });
    res.json(activeAuctions);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Complete Auctions
router.post("/complete", async (req, res) => {
  const { auctionID } = req.body;

  try {
    const auction = await Auction.findById(auctionID);

    if (!auction || auction.status !== "active") {
      return res.status(404).json({ message: "Auction not found or already completed" });
    }

    auction.status = "completed";
    await auction.save();

    res.json({ message: "Auction completed successfully", auction });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

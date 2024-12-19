const mongoose = require("mongoose");

const AuctionSchema = new mongoose.Schema({
  itemID: { type: String, required: true },
  itemName: { type: String, required: true },
  sellerID: { type: String, required: true },
  startingPrice: { type: Number, required: true },
  currentBid: { type: Number, default: 0 },
  currentBidderID: { type: String },
  endTime: { type: Date, required: true },
  status: { type: String, enum: ["active", "completed"], default: "active" },
});

module.exports = mongoose.model("Auction", AuctionSchema);

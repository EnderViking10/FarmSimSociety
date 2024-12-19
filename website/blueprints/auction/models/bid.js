const mongoose = require("mongoose");

const BidSchema = new mongoose.Schema({
  auctionID: { type: mongoose.Schema.Types.ObjectId, ref: "Auction", required: true },
  bidderID: { type: String, required: true },
  amount: { type: Number, required: true },
  timestamp: { type: Date, default: Date.now },
});

module.exports = mongoose.model("Bid", BidSchema);

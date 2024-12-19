const mongoose = require("mongoose");

const ContractSchema = new mongoose.Schema({
  contractID: { type: String, required: true },
  title: { type: String, required: true },
  description: { type: String, required: true },
  status: { type: String, enum: ["open", "accepted", "completed"], default: "open" },
  playerID: { type: String }, // Assigned player
  postedBy: { type: String, required: true },
  createdAt: { type: Date, default: Date.now },
});

module.exports = mongoose.model("Contract", ContractSchema);

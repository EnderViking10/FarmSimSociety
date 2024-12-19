const mongoose = require("mongoose");

const LogSchema = new mongoose.Schema({
  action: { type: String, required: true },
  adminID: { type: mongoose.Schema.Types.ObjectId, ref: "Admin", required: true },
  timestamp: { type: Date, default: Date.now },
  details: { type: Object },
});

module.exports = mongoose.model("Log", LogSchema);

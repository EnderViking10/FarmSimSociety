const express = require("express");
const bodyParser = require("body-parser");
const dotenv = require("dotenv");
const connectDB = require("./config/db");

// Import Routes
const adminRoutes = require("./routes/admin");
const loanRoutes = require("./routes/loans");
const contractRoutes = require("./routes/contracts");
const auctionRoutes = require("./routes/auctions");

// Configure Environment and Database
dotenv.config();
connectDB();

// Initialize Express App
const app = express();

// Middleware
app.use(bodyParser.json());

// API Endpoints
app.use("/api/admin", adminRoutes);
app.use("/api/loans", loanRoutes);
app.use("/api/contracts", contractRoutes);
app.use("/api/auctions", auctionRoutes);

// Start Server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

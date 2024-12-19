const Admin = require("../models/Admin");

const authenticate = async (req, res, next) => {
  const token = req.header("Authorization");

  if (!token) {
    return res.status(401).json({ message: "Unauthorized" });
  }

  try {
    // Simple token check (replace with JWT verification for production)
    const adminID = token.split("-")[1];
    const admin = await Admin.findById(adminID);

    if (!admin) {
      return res.status(401).json({ message: "Unauthorized" });
    }

    req.admin = admin;
    next();
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

module.exports = { authenticate };

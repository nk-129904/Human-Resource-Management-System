const express = require("express");
const router = express.Router();
const User = require("../models/User");
const Counter = require("../models/Counter");

// CREATE EMPLOYEE + AUTO LOGIN ID
router.post("/create-employee", async (req, res) => {
  const { name, email } = req.body;
  const year = new Date().getFullYear();

  let counter = await Counter.findOne({ year });
  if (!counter) counter = await Counter.create({ year, count: 0 });

  counter.count += 1;
  await counter.save();

  const serial = String(counter.count).padStart(4, "0");
  const [f, l] = name.split(" ");

  const loginId =
    "OI" +
    f.substring(0, 2).toUpperCase() +
    l.substring(0, 2).toUpperCase() +
    year +
    serial;

  await User.create({
    name,
    email,
    loginId,
    role: "EMPLOYEE",
  });

  res.json({ loginId });
});

module.exports = router;

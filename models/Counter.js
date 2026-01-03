const mongoose = require("mongoose");

const counterSchema = new mongoose.Schema({
  year: Number,
  count: { type: Number, default: 0 },
});

module.exports = mongoose.model("Counter", counterSchema);

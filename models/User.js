const mongoose = require('mongoose');

// Schema
const userSchema = new mongoose.Schema({
    balance: { type: Number, default: 0 }
})

const User = mongoose.model('user', userSchema);
module.exports = User;
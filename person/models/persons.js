const mongoose = require('mongoose');

const registrationSchema = new mongoose.Schema({
  first_name: {
    type: String,
    trim: true,
  },
  last_name: {
    type: String,
    trim: true,
  },
  company: {
    type: String,
    trim: true,
  },
  address: {
    type: String,
    trim: true,
  },
  salary: {
    type: String,
    trim: true,
  },
  
});

module.exports = mongoose.model('persons', registrationSchema);
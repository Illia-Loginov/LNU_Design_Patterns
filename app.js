const express = require('express');
const mongoose = require('mongoose');
require('dotenv').config();

const app = express();

// Middleware
app.use(express.static(`${__dirname}/public`));
app.use(express.urlencoded({ extended: true }));

// Set view engine
app.set('view engine', 'ejs');

// DB connection and listening to requests
mongoose.connect(process.env.CONNECTION_URL, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => app.listen(process.env.PORT, () => console.log(`App listening on port ${process.env.PORT}...`)))
    .catch(error => console.log('DB connection failed', error));

// Routes
const atmRoutes = require('./routes/atmRoutes');

app.use('/atm', atmRoutes);

// Requests
app.get('/', async (req, res) => {
    res.render('index', { user: undefined, balance: undefined, error: undefined });
});
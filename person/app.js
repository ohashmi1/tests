const express = require('express');
const routes = require('./routes/index');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

app.use(bodyParser.urlencoded({
    extended: true
}));

app.use(bodyParser.urlencoded({ extended: true }));
app.use('/', routes);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

module.exports = app;
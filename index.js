const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const connectDB = require('./config/database');
const morgan = require("morgan");
const port = 4000 || 8080;
require('dotenv').config();

const app = express();
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

connectDB();

app.use(morgan("tiny"));

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header(
        "Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    );

    if (req.method === "OPTIONS") {
        res.header("Access-Control-Allow-Methods", "*");
        return res.status(200).json({});
    }
    next();
});

app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`, '\n');
    console.log(`Headers: ${JSON.stringify(req.headers)}`, '\n');
    console.log(`Body: ${JSON.stringify(req.body)}`, '\n');
    console.log(`Query: ${JSON.stringify(req.query)}`, '\n');
    console.log(`hostname: ${JSON.stringify(req.hostname)}`, '\n');
    next();
});

app.use("/api", require("./routes/Model"));
app.use("/api/users", require("./routes/UserRoute"));

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
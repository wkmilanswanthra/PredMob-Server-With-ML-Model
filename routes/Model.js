const express = require("express");
const route = express.Router();
const axios = require("axios");

route.post("/predict", (req, res) => {
    axios.post("http://localhost:5000/predict", req.body).then((response) => {
        res.status(200).send(response.data);
    }).catch((err) => {
        res.status(500).json({message: err.message || "Server Error"});

    });
});
route.get("/data", (req, res) => {
    axios.get("http://localhost:5000/data", req.body).then((response) => {
        res.status(200).send(response.data);
    }).catch((err) => {
        res.status(500).json({message: err.message || "Server Error"});

    });
});
route.get("/altdata", (req, res) => {
    axios.get("http://localhost:5000/altdata", req.body).then((response) => {
        res.status(200).send(response.data);
    }).catch((err) => {
        res.status(500).json({message: err.message || "Server Error"});

    });
});
route.get("/comparison", (req, res) => {
    axios.get("http://localhost:5000/comparison", req.body).then((response) => {
        res.status(200).send(response.data);
    }).catch((err) => {
        res.status(500).json({message: err.message || "Server Error"});

    });
});

module.exports = route;
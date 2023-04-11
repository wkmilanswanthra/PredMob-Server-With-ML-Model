const mongoose = require("mongoose");
const user = require("../models/User");

exports.createUser = async (req, res) => {
    if (!req.body)
        return res.status(400).send({message: "Request body is required"});

    try {
        const newUser = new user(req.body);
        await newUser.save();
        res.status(201).json({user: newUser});
    } catch (e) {
        res
            .status(500)
            .send({message: e.message || "There was an error saving the user"});
    }
};

exports.getUser = async (req, res) => {
    try {
        const fetchedUser = await user.findById(req.params.id);
        if (!fetchedUser) {
            res.status(404).json({message: "User not found"});
            return;
        }
        res.status(200).json({user: fetchedUser});
    } catch (e) {
        res.status(500).json({message: e.message || "Server Error"});
    }
}

exports.updateUser = async (req, res) => {
    if (!req.body)
        return res.status(400).send({message: "Request body is required"});

    try {
        const updatedUser = await user.findByIdAndUpdate(
            req.params.id,
            req.body,
            {new: true}
        );
        res.status(200).json({user: updatedUser});
    } catch (e) {
        res
            .status(500)
            .send({message: e.message || "There was an error saving the user"});
    }
};
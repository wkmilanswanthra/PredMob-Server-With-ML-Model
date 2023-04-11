const express = require("express");
const route = express.Router();
const userController = require("../controllers/userController");

route.post("/create", userController.createUser);
route.get("/get/:id", userController.getUser);
route.put("/update/:id", userController.updateUser);

module.exports = route;
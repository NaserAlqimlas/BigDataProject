const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const config = require("./config");
const d3 = require("d3");
const Usa = require("./model/america");
const path = require("path");
const exec = require("child_process").exec;
const socket = require("socket.io");
const port = config.app.port;

// in latest body-parser use like below.

mongoose.connect(
  config.db.mongodb,
  {
    useNewUrlParser: true
  },
  error => {
    if (error) {
      console.log(error);
    } else {
      console.log(`Connect to database`);
    }
  }
);

// app.get("/", (req, res) => {
//   res.sendFile(path.join(__dirname + "/usa/index.html"));
// });

app.get("/choropleth", (req, res) => {
  res.sendFile(path.join(__dirname + "/usa/choropleth.html"));
});

app.post("/choropleth", (req, res) => {
  res.redirect("/choropleth");
});

app.get("/us-states", (req, res) => {
  res.sendFile(path.join(__dirname + "/usa/us-states.json"))
})

app.get("/bigdata", (req, res) => {
    Usa.find({}).then(users => {
      res.send([users[users.length - 1]]);
    });
});

const server = app.listen(port, () => console.log(`Example app listening on port ${port}!`));

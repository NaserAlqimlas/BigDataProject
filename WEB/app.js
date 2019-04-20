const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const config = require("./config");
const d3 = require("d3");
const Usa = require("./model/america");
const path = require("path");
const exec = require("child_process").exec;
const port = config.app.port;

// in latest body-parser use like below.
app.use(
  bodyParser.urlencoded({
    extended: true
  })
);

app.use(bodyParser.json());

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

// function create() {
//   Usa.create(
//     {
//       AL: 10000000,
//       AK: 0,
//       AZ: 1,
//       AR: 0,
//       CA: 10000,
//       CO: 500,
//       CT: 0,
//       DE: 1,
//       FL: 500,
//       GA: 0,
//       HI: 1,
//       ID: 4,
//       IL: 0,
//       IN: 0,
//       IA: 0,
//       KS: 1,
//       KY: 1,
//       LA: 1000000,
//       ME: 2,
//       MD: 4,
//       MA: 12,
//       MI: 9,
//       MN: 500,
//       MS: 7,
//       MO: 80000,
//       MT: 34,
//       NE: 4,
//       NV: 6,
//       NH: 4,
//       NJ: 34,
//       NM: 2,
//       NY: 34,
//       NC: 7,
//       ND: 6,
//       OH: 54,
//       OK: 3,
//       OR: 5,
//       PA: 600,
//       RI: 5,
//       SC: 2,
//       SD: 6,
//       TN: 4,
//       TX: 23,
//       UT: 67,
//       VT: 23,
//       VA: 43,
//       WA: 54,
//       WV: 12,
//       WI: 44,
//       WY: 66
//     },
//     (error, data) => {
//       if (error) {
//         console.log(`Error Happen ${error}`);
//       } else {
//         console.log(`Data created successfully${data}`);
//       }
//     }
//   );
// }

// const data = usa.find({}, (error, data) => {
//   if(error){
//     console.log(`Can't find data ${error}`)
//   }else{
//     return data
//   }
// })

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname + "/usa/index.html"));
});

app.get("/choropleth", (req, res) => {
  res.sendFile(path.join(__dirname + "/usa/choropleth.html"));
});

app.post("/choropleth", (req, res) => {
  let keyword = req.body.keyword;
  console.log(keyword);
  // 執行 cat child_process.js 指令：
  //May not work in Heroku
  exec(
    "gcloud dataproc jobs submit pyspark --cluster=cluster-56f5 --region=us-west1 data_processing.py -- " +
      keyword,
    function(error, stdout, stderr) {
      if (error) {
        console.log(error);
      }
      console.info("cat child_process.js stdout: ");
      console.log(stdout);
      // setTimeout(function() {
      //   res.redirect("/choropleth");
      // }, 60000);
      res.redirect("/choropleth");
    }
  );
  //Store this data to the mongoDB database for Spark query
});

app.get("/us-states", (req, res) => {
  res.sendFile(path.join(__dirname + "/usa/us-states.json"));
});

//Get the last item from MongoDB
app.get("/bigdata", (req, res) => {
  Usa.find({}).then(users => {
    res.send([users[users.length - 1]]);
  });
});
// Trying to get keyword from search bar
// app.post("/keyword-route", (req, res) => {
//   if (typeof req.body.keyword === "undefined") {
//     res.status(400).json({ error: "missing parameter keyword", data: null });
//     return;
//   }
//
//   let keyword = req.body.keyword;
//   res.status(200).json({ error: null, data: bar });
// });

app.listen(port, () => console.log(`Example app listening on port ${port}!`));

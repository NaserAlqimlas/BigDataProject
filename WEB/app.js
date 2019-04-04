const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const mongoose = require('mongoose')
const config = require('./config')
const Usa = require('./model/america')
const port = config.app.port

mongoose.connect(config.db.mongodb, {
  useNewUrlParser: true
}, (error) => {
  if(error){
    console.log(error)
  }else{
    console.log(`Connect to database`)
  }
})

// usa.create({
//   AL: 1,
//   AK: 0,
//   AZ: 1,
//   AR: 0,
//   CA: 1,
//   CO: 0,
//   CT: 0,
//   DE: 1,
//   FL: 0,
//   GA: 0,
//   HI: 1,
//   ID: 0,
//   IL: 0,
//   IN: 0,
//   IA: 0,
//   KS: 1,
//   KY: 1,
//   LA: 1,
//   ME: 2,
//   MD: 4,
//   MA: 12,
//   MI: 9,
//   MN: 5,
//   MS: 7,
//   MO: 8,
//   MT: 34,
//   NE: 45,
//   NV: 6,
//   NH: 4,
//   NJ: 34,
//   NM: 2,
//   NY: 34,
//   NC: 7,
//   ND: 6,
//   OH: 54,
//   OK: 3,
//   OR: 5,
//   PA: 6,
//   RI: 5,
//   SC: 2,
//   SD: 6,
//   TN: 4,
//   TX: 23,
//   UT: 67,
//   VT: 23,
//   VA: 43,
//   WA: 54,
//   WV: 12,
//   WI: 44,
//   WY: 66
//
// }, (error, data) => {
//   if(error){
//     console.log(`Error Happen ${error}`)
//   }else{
//     console.log(`Data created successfully${data}`)
//   }
// })

// const data = usa.find({}, (error, data) => {
//   if(error){
//     console.log(`Can't find data ${error}`)
//   }else{
//     return data
//   }
// })

app.get('/bigdata', (req, res) => {
  Usa.find({}).then((users) => {
    res.send(users)
  })
})


app.listen(port, () => console.log(`Example app listening on port ${port}!`))

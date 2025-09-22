/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */
import express from "express"
import dotenv from "dotenv";
import cors from "cors";
import { MongoClient } from "mongodb";

dotenv.config();

// Create express server
const server = express();
const port = 3000;

//Cors error handling
server.use(cors());

  //Connect to database
const connectionString = process.env.URI;
const client = new MongoClient(connectionString);
await client.connect();

//Start server
server.listen(port, () => {
console.log(`Server is listening on port ${port}`);
});

// -------------------- ROUTES ------------------------ //
server.get('/', (request, response) => {
      response.send("Testing Home Page");
    });

server.get('/houses', async (request, response) => {
  try{
    const database = client.db("KingstonHouses");
    const collection = database.collection("Houses_One");

    const cursor = collection.find({});
    let houseList = [];

    for await (const doc of cursor){ // Clean up so only the following information goes to the site. 
      houseList.push({
        address: doc.Address,
        price: doc.Price,
        type: doc.Property_Type,
        image: doc.Img_Link
      });
    }
    response.json(houseList);

  }catch (error) {
    console.error(error);
    response.status(500).send("Error retrieving data")
  }
})

//ToDo

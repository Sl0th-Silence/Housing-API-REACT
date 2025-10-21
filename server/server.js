/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */
import express from "express"
import cors from "cors";
import { MongoClient } from "mongodb";
import dotenv from 'dotenv';

dotenv.config({path:'server\\.env'})
// Create express server
const server = express();
const port = 3000;

//Cors error handling
//Used for when you are launching both an express and react server
server.use(cors());

  //Connect to database
const connection = (process.env.MONGO_URL);
(connection) ? console.log("Connection with MONGO made") : console.log("Connection not made");
const client = new MongoClient(connection);
await client.connect();

//Start server
server.listen(port, () => {

console.log(`Server is listening on port ${port}`);
}); 

// -------------------- ROUTES ------------------------ //
server.get('/houses', async (request, response) => {
  try{
    const database = client.db("KingstonHouses");
    const collection = database.collection("Houses_One_2025_SEPT_25");

    const cursor = collection.find({});
    let houseList = [];

    for await (const doc of cursor){ // Clean up so only the following information goes to the site. 
      houseList.push({
        id: doc._id,
        address: doc.Address,
        price: doc.Price,
        type: doc.Property_Type,
        image: doc.Img_Link
      });
    }
    response.json(houseList);
    console.log("Success") //Response worked

  }catch (error) {
    console.error(error);
    response.status(500).send("Error retrieving data")
    console.log("Error") //Response Failed
  }
})

//ToDo

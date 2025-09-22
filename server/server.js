/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */
import express from "express"
import dotenv from "dotenv";
import cors from "cors";

dotenv.config();

// Create express server
const server = express();
const port = 3000;

//Cors error handling
server.use(cors());

//Connect to database
import { MongoClient } from "mongodb";
const connectionString = process.env.URI;
if(!connectionString)
{
    console.log("No Connection String")
}
const client = new MongoClient(connectionString);
await client.connect();

//Start server
server.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
})

//Home
server.get('/', (request, response) => {
      response.send("Hey");
    });

server.get('/houses', async (request, response) => {
  
  try{
    const database = client.db("KingstonHouses");
    const collection = database.collection("Houses_One");

    const cursor = collection.find({});
    let userList = [];
    let counter = 0;

    for await (const doc of cursor){ // Clean up so only the following information goes to the site. 
      userList.push({
        address: doc.Address,
        price: doc.Price,
        type: doc.Property_Type,
        image: doc.Img_Link
      });
      counter+=1;
    }
    response.json(userList);

  }catch (error) {
    console.error(error);
    response.status(500).send("Error retrieving data")
  }
})

//ToDo
// Connect to database and organize information

//After connecting, we will try and iterate through the db
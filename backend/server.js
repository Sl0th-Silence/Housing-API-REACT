import express from "express";
import cors from "cors";
import mongoose from "mongoose";
import dotenv from "dotenv";

//Import model
import House from "./models/house.js";

dotenv.config();
const { MONGO_DBI } = process.env;
const server = express();
const port = 3000;

//Middleware
server.use(cors());
server.use(express.json());
server.use(express.urlencoded({ extended: true }));

//Connect to mongoose
mongoose
  .connect(MONGO_DBI)
  .then(() => {
    server.listen(port, () => {
      console.log(`Connected to database\nServer is listening on port ${port}`);
    });
  })
  .catch((error) => console.log(error));

//routes

//Main route
server.get("/", (request, response) => {
  response.send("Server is live");
});

// -------------------- ROUTES ------------------------ //
server.get("/houses", async (request, response) => {
  try {
    const documents = await House.find({});

    let houseList = [];

    // Clean up so only the following information goes to the site.
    houseList = documents.map((doc) => ({
      id: doc._id,
      address: doc.Address,
      price: doc.Price,
      type: doc.Property_Type,
      image: doc.Img_Link,
    }));
    response.json(houseList);
    console.log("Success"); //Response worked
  } catch (error) {
    console.error(error);
    response.status(500).send("Error retrieving data");
    console.log("Error"); //Response Failed
  }
});

//ToDo

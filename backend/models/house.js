import mongoose from "mongoose";

const houseSchema = new mongoose.Schema({
  Address: String,
  Price: Number,
  Property_Type: String,
  Img_Link: String,
});

export default mongoose.model("House", houseSchema);

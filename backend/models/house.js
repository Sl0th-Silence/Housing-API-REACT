import mongoose from "mongoose";

const houseSchema = new mongoose.Schema(
  {
    Address: String,
    Price: Number,
    Property_Type: String,
    Img_Link: String,
  },
  { collection: "Houses_One" } //Making sure to use the correct collection
);

export default mongoose.model("House", houseSchema);

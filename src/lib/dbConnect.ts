import mongoose from "mongoose";
import dotenv from "dotenv";
dotenv.config({ path: "../.env" });

type ConnectionObject = {
  isConnected?: number;
};
const connection: ConnectionObject = {};

export default async function dbConnect(): Promise<void> {
  if (connection.isConnected) {
    console.log("[+] Already connected to database");
    return;
  }

  try {
    //! connected using mongoURI string or an empty string, {} is options fields
    const db = await mongoose.connect("mongodb+srv://harshitabarnwal:Harshita@cluster1.sludnrg.mongodb.net/SRS" , {});
    connection.isConnected = db.connections[0].readyState;
    console.log("[+] DB Connected Successfully");
  } catch (error) {
    console.log("[-] Database Connection Failed", error);
    process.exit(1);
  }
}

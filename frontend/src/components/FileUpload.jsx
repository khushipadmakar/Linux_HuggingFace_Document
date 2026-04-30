import {useState} from "react";
import {uploadDocument} from "../services/api";

export default function FileUpload(){

const [file,setFile]=useState();

const uploadFile=async()=>{
 if (!file) {
  return;
 }

 await uploadDocument(file);
};

return(
<div>
<input
type="file"
onChange={(e)=>setFile(e.target.files[0])}
/>

<button onClick={uploadFile}>
 Upload
</button>
</div>
);
}
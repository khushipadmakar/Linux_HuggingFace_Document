import {useState} from "react";
import axios from "axios";

export default function FileUpload(){

const [file,setFile]=useState();

const uploadFile=async()=>{
 let formData=new FormData();
 formData.append("file",file);

 await axios.post(
  "http://localhost:8000/upload",
   formData
 );
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
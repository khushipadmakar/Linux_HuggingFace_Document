import {useState} from "react";

export default function useUpload(){

const [loading,setLoading]=useState(false);

return {loading};
}
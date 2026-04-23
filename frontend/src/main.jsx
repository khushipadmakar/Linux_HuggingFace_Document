import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/app.css";

const root = document.getElementById("root");
if (!root) {
  throw new Error("Root element not found");
}
console.log("Starting React app");
ReactDOM.createRoot(root).render(<App />);

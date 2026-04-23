import {Link} from "react-router-dom";

export default function Navbar(){
 return(
  <nav>
   <Link to="/">Dashboard</Link> |
   <Link to="/documents">Documents</Link> |
   <Link to="/search">Search</Link> |
   <Link to="/qa">Q&A</Link>
  </nav>
 );
}
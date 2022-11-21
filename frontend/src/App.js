import './App.css';
import { BrowserRouter } from "react-router-dom"
function App() {
  return (
    <div>
      <a href="http://localhost:8001/api/v1/auth/login">Click here to login!</a>
      <br></br>
      You are not logged in
      <br></br>
      <a href="https://otl.kaist.ac.kr/session/info">logged in?</a>
    </div>
  );
  // return (
  //   <BrowserRouter>
  //     <Routes>

  //     </Routes>
  //   <BrowserRouter />
  // )
}

export default App;

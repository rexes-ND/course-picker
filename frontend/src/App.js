import './App.css';
import LoginPage from './components/LoginPage'
import HomePage from './components/HomePage'
import { BrowserRouter, Routes, Route, redirect } from "react-router-dom"
import { useEffect, useState } from 'react';
import axios from 'axios';

const instance = axios.create({
  withCredentials: true,
})
function App() {
  const [login, setLogin] = useState(null)
  useEffect(() => {
    instance.post("http://localhost:8001/api/v1/auth/status")
    .then((res) => {
      console.log(res.data)
      if (res.data['status'] === 200) {
        setLogin(true)
      } else {
        setLogin(false)
        redirect('/login')
      }
    })
    .catch((error) => {
      console.log(error)
    })
  }, [])
  
  if (login === null){
    return (
      <></>
    )
  }
  // return (
  //   <div>
  //     {login?(<a href="http://localhost:8001/api/v1/auth/logout?next=http://localhost:3000">LOG OUT</a>):(<a href="http://localhost:8001/api/v1/auth/login?next=http://localhost:3000">LOG IN</a>)}
  //   </div>
  // );
  
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path='/' element={login?<HomePage/>:<LoginPage/>} />
        <Route exact path='/login' element={<LoginPage/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;

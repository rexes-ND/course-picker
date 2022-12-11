import LoginPage from './components/LoginPage'
import HomePage from './components/HomePage'
import UserPage from './components/UserPage'
import GenerateSchedulePage from './components/GenerateSchedulePage'
import SavedSchedulesPage from './components/SavedSchedulesPage'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { useEffect, useState } from 'react';
import instance from '../src/Client'
import styled from 'styled-components';

const Container = styled.div`
  font-family: 'Lato', sans-serif;
`

function App() {
  const [login, setLogin] = useState(null)
  const [user, setUser] = useState({
    "studentID": '',
    "majorType": null,
    "major": null,
    "minor": null,
    "firstName": '',
    "lastName": '',
  })
  useEffect(() => {
    instance.post("http://localhost:8001/api/v1/auth/status")
    .then((res) => {
      console.log(res.data)
      if (res.data['status'] === 200) {
        setLogin(true)
      } else {
        setLogin(false)
      }
    })
    .catch((error) => {
      console.log(error)
    })
  }, [])
  useEffect(() => {
    if (login && user.studentID === ''){
      console.log("Erkhes")
      instance.get('http://localhost:8001/api/v1/auth/user')
        .then(res => {
          console.log(res.data)
          if (res.data["status"] === 200){
              setUser({
                  "studentID": res.data["student_id"],
                  "majorType": (res.data["major_type"] === null)?"":res.data["major_type"],
                  "major": res.data["major"],
                  "minor": res.data["minor"],
                  "firstName": res.data["first_name"],
                  "lastName": res.data["last_name"],
              })
          } else {
              setLogin(false)
          }
        })
        .catch(error => {
            console.log(error)
        })
    }
}, [user, login])  


  if (login === null || (login === true && user.studentID === '')){
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
    <Container>
      <BrowserRouter>
        <Routes>
          <Route exact path='/' element={login?<HomePage login={login} user={user} setUser={setUser} setLogin={setLogin}/>:<LoginPage/>} />
          <Route exact path='/login' element={<LoginPage/>} />
          <Route exact path='/user' element={login?<UserPage login={login} user={user} setUser={setUser} setLogin={setLogin}/>:<LoginPage/>} />
          <Route exact path='/generate' element={login?<GenerateSchedulePage login={login} user={user} setUser={setUser} setLogin={setLogin}/>:<LoginPage/>} />
          <Route exact path='/saved' element={login?<SavedSchedulesPage login={login} user={user} setUser={setUser} setLogin={setLogin}/>:<LoginPage/>} />
        </Routes>
      </BrowserRouter>
    </Container>
  )
}

export default App;

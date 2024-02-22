import React from 'react'
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import {useState, useEffect} from 'react'

import './App.css'
import Login from './components/Login/Login'
import Rooms from './components/Rooms/Rooms'
import Test from './components/Test/Test'
import Draw from './components/Draw/Draw'

function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [name, setName] = useState("")

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {/* <Route path="/" element={<Test />} /> */}
          <Route path="/" element={<Login setLoggedIn={setLoggedIn} setName={setName} />} />
          <Route path="/rooms" element={<Rooms loggedIn={loggedIn} name={name} />} />
          <Route path="/draw" element={<Draw loggedIn={loggedIn} name={name} />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}


export default App
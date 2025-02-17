import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [users, setUsers] = useState([])  // Stan dla listy użytkowników

  const handleAddUser = async () => {
    const response = await fetch('http://localhost:5001/api/add_user', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        email: email,
      }),
    })

    const data = await response.json()
    if (response.ok) {
      alert(data.message)
      fetchUsers()  // Odśwież listę użytkowników po dodaniu
    } else {
      alert(`Error: ${data.error || 'Something went wrong'}`)
    }
  }

  const fetchUsers = async () => {
    const response = await fetch('http://localhost:5001/api/users')
    const data = await response.json()
    setUsers(data)  // Ustawienie użytkowników w stanie
  }

  useEffect(() => {
    fetchUsers()  // Pobiera listę użytkowników zaraz po załadowaniu komponentu
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>

      <div>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button onClick={handleAddUser}>Add User</button>
      </div>

      <h2>Users List</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            {user.username} - {user.email}
          </li>
        ))}
      </ul>

      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App

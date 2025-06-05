import { useState } from 'react'
import './App.css'
import backendUrl from './config'

export function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  return match ? match[2] : null
}

function LoginForm() {
  const [username, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [loggedIn, setLoggedIn] = useState(!!getCookie('access_token'))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${backendUrl}/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })
      if (!res.ok) throw new Error('Invalid credentials')
      const data = await res.json()
      if (!data.access) throw new Error('No token received')
      const expires = new Date(Date.now() + 5 * 60 * 1000).toUTCString()
      document.cookie = `access_token=${data.access}; expires=${expires}; path=/`
      setLoggedIn(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loggedIn) {
    return <div style={{marginTop: 32, color: '#222', fontWeight: 500}}>You are logged in.</div>
  }

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <h3>Login</h3>
      <div>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
      {error && <div className="error">{error}</div>}
    </form>
  )
}

export default LoginForm

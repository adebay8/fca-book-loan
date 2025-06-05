import { useState } from 'react'
import './App.css'
import BookList from './BookList'
import Wishlist from './Wishlist'
import LoginForm from './LoginForm'

function App() {
  const [tab, setTab] = useState('login')
  return (
    <div className="container">
      <div className="tabs">
        <button className={tab === 'login' ? 'active' : ''} onClick={() => setTab('login')}>Login</button>
        <button className={tab === 'books' ? 'active' : ''} onClick={() => setTab('books')}>Books</button>
        <button className={tab === 'wishlist' ? 'active' : ''} onClick={() => setTab('wishlist')}>Wishlist</button>
      </div>
      <div className="tab-content">
        {tab === 'login' && <LoginForm />}
        {tab === 'books' && <BookList />}
        {tab === 'wishlist' && <Wishlist />}
      </div>
    </div>
  )
}

export default App

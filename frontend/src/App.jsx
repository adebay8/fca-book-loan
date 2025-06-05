import { useState } from 'react'
import './App.css'
import BookList from './BookList'
import Wishlist from './Wishlist'

function App() {
  const [tab, setTab] = useState('books')
  console.log('Current tab:', tab)
  return (
    <div className="container">
      <div className="tabs">
        <button className={tab === 'books' ? 'active' : ''} onClick={() => setTab('books')}>Books</button>
        <button className={tab === 'wishlist' ? 'active' : ''} onClick={() => setTab('wishlist')}>Wishlist</button>
      </div>
      <div className="tab-content">
        {tab === 'books' && <BookList />}
        {tab === 'wishlist' && <Wishlist />}
      </div>
    </div>
  )
}

export default App

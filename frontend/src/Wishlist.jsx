import { useState, useEffect } from 'react'
import backendUrl from './config'
import { getCookie } from './LoginForm'

function Wishlist() {
  const [wishlist, setWishlist] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(!!getCookie('access_token'))

  useEffect(() => {
    if (!isAuthenticated) return
    setLoading(true)
    setError(null)
    fetch(`${backendUrl}/catalog/wishlist/`, {
      headers: {
        Authorization: `Bearer ${getCookie('access_token')}`
      }
    })
      .then(res => {
        if (res.status === 401) {
          setIsAuthenticated(false)
          setLoading(false)
          return
        }
        if (!res.ok) throw new Error('Failed to fetch wishlist')
        return res.json()
      })
      .then(data => {
        if (data) setWishlist(data.books || [])
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [isAuthenticated])

  return !isAuthenticated ? (
    <div style={{marginTop: 32, color: '#d32f2f', fontWeight: 500}}>
      You must be logged in to view your wishlist.
    </div>
  ) : (
    <div>
      <h2>Wishlist</h2>
      {loading && <p>Loading...</p>}
      {error && <p style={{color: 'red'}}>{error}</p>}
      <ul>
        {wishlist.length === 0 && !loading && <li>No books in wishlist.</li>}
        {wishlist.map(book => (
          <li key={book.id}>
            <strong>{book.title}</strong> by {book.authors && book.authors.join(', ')}<br/>
            ISBN: {book.isbn}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Wishlist

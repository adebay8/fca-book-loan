import { useState, useEffect } from 'react'
import backendUrl from './config'

function Wishlist() {
  const [wishlist, setWishlist] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetch(`${backendUrl}/catalog/wishlist/`, { credentials: 'include' })
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch wishlist')
        return res.json()
      })
      .then(data => {
        setWishlist(data.books || [])
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
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

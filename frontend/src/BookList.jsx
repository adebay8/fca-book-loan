import { useState, useEffect } from 'react'
import backendUrl from './config'

function BookList() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetch(`${backendUrl}/catalog/books/`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch books')
        return res.json()
      })
      .then(data => {
        setBooks(data || [])
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div>
      <h2>Book Catalog</h2>
      {loading && <p>Loading...</p>}
      {error && <p style={{color: 'red'}}>{error}</p>}
      <ul>
        {books.map(book => (
          <li key={book.id}>
            <strong>{book.title}</strong> by {book.authors && book.authors.join(', ')}<br/>
            ISBN: {book.isbn} | Year: {book.publication_year} | Language: {book.language}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default BookList

import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState('Checking...')

  useEffect(() => {
    // Fetch from the *relative* /api path
    // Vite will proxy this to your Fedora server
    fetch('/health') // Assuming this is a valid endpoint
      .then(res => res.json())
      .then(data => {
        setApiStatus(JSON.stringify(data))
      })
      .catch(err => {
        console.error(err)
        setApiStatus('Failed to fetch from API')
      })
  }, [])

  return (
    <div className="App">
      <h1>Fedora DevOps Lab Frontend</h1>
      <p>
        <strong>API Status:</strong> {apiStatus}
      </p>
    </div>
  )
}

export default App
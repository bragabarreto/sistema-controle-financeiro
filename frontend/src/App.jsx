import { useState } from 'react'
import Layout from './components/layout/Layout'
import DashboardSimple from './components/DashboardSimple'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('/')

  const renderPage = () => {
    switch (currentPage) {
      case '/':
        return <DashboardSimple />
      default:
        return <DashboardSimple />
    }
  }

  return (
    <Layout currentPath={currentPage}>
      {renderPage()}
    </Layout>
  )
}

export default App

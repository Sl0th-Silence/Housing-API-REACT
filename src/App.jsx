import './App.css'
import HouseList from './components/importData'
import Greeting from './components/greeting'

function App() {
  return (
    <>
      <h1 className="title">Kingston Housing Sales</h1>
      <h2 className='author'>Jay Mills</h2>
      <HouseList />
    </>
  )
}

export default App

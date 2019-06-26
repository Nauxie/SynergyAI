import React from 'react';
import Hero from './components/Hero'
import './App.css';
import hlist from './data/Heroes'




const list = hlist.map(list => {
  return(<Hero hero= {list}/>)
})

function App() {
  return (
    <div className="App">
      <header className="App-header">
        
        {list}
      </header>
    </div>
  );
}

export default App;

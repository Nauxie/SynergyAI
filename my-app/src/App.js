import React from 'react';
import Hero from './components/Hero'
import './App.css';
import hlist from './data/Heroes'




const list = hlist.map(list => {
  return(<Hero hero= {list} key={list.id}/>)
})

function App() {
  return (
    <div className="page">
      <header>
        
        {list}
      </header>
    </div>
  );
}

export default App;

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
      <div className="namecenter">
        <a href="https://underlords.com/">
        <img src="https://cdn-www.bluestacks.com/bs-images/Logo508.png" alt="logo" width="250px"/>
        </a>
        
      </div>
      <header>
        
        {list}
      </header>
    </div>
  );
}

export default App;

import React from 'react';
import HeroCard from './components/HeroCard'
import hlist from './data/Heroes'

import Shop from './components/Shop'

import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      search: ''
    }
  }
  updateSearch(event) {
    this.setState({ search: event.target.value });
  }
  render() {
    let filteredhlist = hlist.filter(
      (hero) => {
        return hero.name.toLowerCase().includes(this.state.search.toLowerCase())
      }
    )
    const list = filteredhlist.map(list => {
      return (<HeroCard hero={list} key={list.id} />)
    })
    return (
      <div className="page">
        <div className="namecenter">
          <a href="https://underlords.com/">
            <img src="https://cdn-www.bluestacks.com/bs-images/Logo508.png" alt="logo" width="250px" />
          </a>
        </div>
        <div>
          <Shop />
        </div>
        <div>
          {/*-- <div className="searchbar">
            <input type="text" placeholder="Search..." value={this.state.search} onChange={this.updateSearch.bind(this)} />
          </div>  
    */}
        </div>
    {list}
      </div>
    )
  }
}
export default App;

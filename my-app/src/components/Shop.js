import React from 'react'
import HeroMiniCard from './HeroMiniCard'
import hlist from '../data/Heroes'

class Shop extends React.Component {
    constructor(props) {
        super(props)
        this.test = this.test.bind(this)
        this.updateSearch = this.updateSearch.bind(this)
        this.state = {
            search: '',
            bench: [],
        }
    }
    test(a) {
        console.log(a)
    }
    updateSearch(event) {
        this.setState({ search: event.target.value });
    }
    render() {
        let filteredhlist = hlist.filter(
            (hero) =>
                hero.name.toLowerCase().includes(this.state.search.toLowerCase())
        )
        const flist = filteredhlist.map(list =>
            (<HeroMiniCard hero={list} key={list.id} test={this.test} />)
        )

        return (
            <div>
                <div>
                    <input type="text" placeholder="Search..." value={this.state.search} onChange={this.updateSearch} />
                    {flist}
                </div>
                <div>

                </div>

            </div>


        )
    }
}

export default Shop
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
            //benchnames: [],
            benchObjs: [],
        }
    }
    test(a, b) {
        //this.state.benchnames.push(a)
        //console.log(this.state.benchnames)
        //this.state.benchObjs.push(hlist.find((obj) => obj.name === a))
        if (b) {
            //var removed = this.state.benchObjs.filter(item => item !== hlist.find((obj) => obj.name === a))
            var removed = this.state.benchObjs
            for ( var i = 0; i < removed.length; i++) {
                if (removed[i].name === a) {
                    removed.splice(i,1)
                    break

                }
            }
            this.setState({
                benchObjs: removed,
            })
        }
        else {
            if (this.state.benchObjs.length === 8) {
                alert("Max of eight heroes in the bench!")
            }
            else {
                var joined = this.state.benchObjs.concat(hlist.find((obj) => obj.name === a))
                this.setState({
                    benchObjs: joined,
                })
            }

        }

        //console.log(this.state.benchObjs)
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
            (<HeroMiniCard hero={list} key={list.id} test={this.test} benchStat={false} />)
        )
        //find the object in hlist that matches the elements in this.state.benchnames and push it to an array with that object
        const benchlist = this.state.benchObjs.map(list =>
            (<HeroMiniCard hero={list} key={list.id} test={this.test} benchStat={true} />)
        )
        return (
            <div>
                <input type="text" placeholder="Search..." value={this.state.search} onChange={this.updateSearch} />
                <div className="shoplist">
                    {flist}
                    <div className="container2">
                        <div className="bench">
                            {benchlist}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
export default Shop
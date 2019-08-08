import React from 'react'
import HeroMiniCard from './HeroMiniCard'
import hlist from '../data/Heroes'

class Shop extends React.Component {
    constructor(props) {
        super(props)
        this.test = this.test.bind(this)
        this.updateSearch = this.updateSearch.bind(this)
        this.clear = this.clear.bind(this)

        this.state = {
            search: '',
            shopObjs: [],

        }

    }
    test(a, b, c) { //test(antimage,true)
        //this.state.benchnames.push(a)
        //console.log(this.state.benchnames)
        //this.state.benchObjs.push(hlist.find((obj) => obj.name === a))
        if (b) {
            //var removed = this.state.benchObjs.filter(item => item !== hlist.find((obj) => obj.name === a))
            var removed = this.state.shopObjs
            for (var i = c; i < removed.length; i++) {
                if (removed[i].name === a) {

                    removed.splice(i, 1)
                    break
                }
            }
            this.setState({
                shopObjs: removed,
            })
        }
        else {
            if (this.state.shopObjs.length === 5) {
                
                alert("Max of five heroes in the shop!")
            }
            else {
                var joined = this.state.shopObjs.concat(hlist.find((obj) => obj.name === a))
                this.setState({
                    shopObjs: joined,
                })
            }

        }

    }
    updateSearch(event) {
        this.setState({ search: event.target.value })
    }
    clear() {
        this.setState(
            {
                shopObjs: []
            }
        )

    }
    clearButton() {
        if (this.state.shopObjs.length === 0) {
            return <h2 className="whitetext">Add the five heroes in your shop.</h2>

        }
        else {
            return (<button className="clearbutton" onClick={this.clear}>Clear</button>)
        }
    }
    predictButton() {
        if (this.state.shopObjs.length === 5) {
            let a = ""
            for (let i = 0; i<5;i++) {
                if (i === 4) {
                    a = a + this.state.shopObjs[i].name 
                }
                else {
                    a = a + this.state.shopObjs[i].name + ',' 
                }   
            }
            return (<button className="clearbutton" >Predict</button>)
        }
        else {
            return null
        }
    }


    render() {
        let filteredhlist = hlist.filter(
            (hero) =>
                hero.name.toLowerCase().includes(this.state.search.toLowerCase())
        )
        const flist = filteredhlist.map(list =>
            (<HeroMiniCard hero={list} key={list.id} test={this.test} shopStat={false} />)
        )
        //find the object in hlist that matches the elements in this.state.benchnames and push it to an array with that object\


        let id = -1
        function generate_id() {
            id++
            return (id)
        }
        let key = -1
        function generate_key() {
            key++
            return (key)
        }

        let shoplist = this.state.shopObjs.map(list =>
            (<HeroMiniCard hero={list} key={generate_key()} test={this.test} shopStat={true} id={generate_id()} />)
        )
        return (
            <div className="entireshop">
                <input className="searchlist" type="text" placeholder="Search..." value={this.state.search} onChange={this.updateSearch} />
                <div className="shoplist">
                    {flist}
                </div>
                <div className="shopandclear">
                    <div className="shopheroes">
                        {shoplist}
                    </div>
                    {this.clearButton()}
                    {this.predictButton()}
                    
                </div>
                
                

            </div>
        )
    }
}
export default Shop
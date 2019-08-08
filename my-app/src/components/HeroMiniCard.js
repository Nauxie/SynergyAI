import React from 'react'

class HeroMiniCard extends React.Component {

    constructor(props) {
        super(props)

        this.state = {

        }
        this.handleClick = this.handleClick.bind(this)
    }
    handleClick() {
        this.props.test(this.props.hero.name,this.props.shopStat,this.props.id)
        //console.log(this.props.hero.name)
    }
    rightClick() {
        console.log("hello")
    }
    render() {
        const imgurl = "http://cdn.dota2.com/apps/dota2/images/heroes/" + this.props.hero.truename + "_full.png?v=5194393";
        const imgurl2 = imgurl.toLowerCase()
        //const passName = this.props.hero.name;
        //console.log(passName)
        return (       
                <div className="scene2">
                    <div className="box" onClick={this.handleClick} onContextMenu={this.rightClick}>
                        <img className="imgstyle2" src={imgurl2} alt={this.props.hero.name} width='50px'></img>
                    </div>
                </div>

        )
    }

}
export default HeroMiniCard

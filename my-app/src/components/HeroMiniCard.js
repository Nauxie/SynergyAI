import React from 'react'

class HeroMiniCard extends React.Component {

    constructor(props) {
        super(props)

        this.state = {

        }
        this.handleClick = this.handleClick.bind(this)

    }
    handleClick() {
        this.props.test(this.props.hero.name,this.props.benchStat)
        //console.log(this.props.hero.name)
    }

    render() {
        
        
        const imgurl = "http://cdn.dota2.com/apps/dota2/images/heroes/" + this.props.hero.truename + "_full.png?v=5194393";
        const imgurl2 = imgurl.toLowerCase()
        //const passName = this.props.hero.name;
        //console.log(passName)

        return (
            
                <div className="scene2" onClick={this.handleClick}>
                    <div className="imgstyle2">
                        <img src={imgurl2} alt={this.props.hero.name} width='50px'></img>
                    </div>

                </div>

            
        )
    }

}
export default HeroMiniCard

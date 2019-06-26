import React from 'react'

class HeroCard extends React.Component {
    constructor(props) {
        super(props)
        this.toggleClass = this.toggleClass.bind(this)
        this.state = {
            class: 'card',
        }

    }


    toggleClass() {
        

        if (this.state.class === 'card') {
            this.setState({ class:'card is-flipped'})
            
        }
            

        else if (this.state.class === "card is-flipped") {
            this.setState({ class:'card'})
            
        }
    }

    render() {
        const name = this.props.hero.truename.split(' ').join('_');
        const imgurl = "http://cdn.dota2.com/apps/dota2/images/heroes/" + name + "_full.png?v=5194393?v=5194393";
        const imgurl2 = imgurl.toLowerCase();
        var typer
        
        
        if (this.props.hero.type3 == null) {
            typer = this.props.hero.type1.trim() + " | " + this.props.hero.type2.trim()
            
        }
        else {
            typer = this.props.hero.type1.trim() + " | " + this.props.hero.type2.trim() + " | " + this.props.hero.type3.trim() 
        }

        return (

            <div className="scene">
                <div className={this.state.class} onClick={this.toggleClass}>
                    <div className = "card__face card__face--front">
                        <div className="imgstyle">
                            <img src={imgurl2} alt="icon" width='90px'  vspace="10px"></img>
                        </div>
                        <div className="namecenter">
                            <b>{this.props.hero.name}</b>
                            
                        </div>
                    </div>
                    <div className="card__face card__face--back">
                        <div className="container">
                            <div className="inner">
                            <b>{typer}</b>
                                <div className="child">
                                    <p> HP: {this.props.hero.Health} </p>
                                    <p>DPS: {this.props.hero.DPS}</p>
                                    <p>Range: {this.props.hero.Attack_Range}</p>
                                    <p> Armor: {this.props.hero.Armor} </p>
                                </div>
                                
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        )
    }

}
export default HeroCard


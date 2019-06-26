import React from 'react'

function Hero(props) { // props = list
    return (
        <div className ="hero">
            <h1>{props.hero.name}</h1> 
            <h4>{props.hero.type1} + {props.hero.type2}</h4>
            <hr/>
        </div>

    )
}
export default Hero


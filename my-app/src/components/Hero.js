import React from 'react'

function Hero(props) { // props = list
    const name = props.hero.name.split(' ').join('_');
    const imgurl = "http://cdn.dota2.com/apps/dota2/images/heroes/" + name + "_full.png?v=5194393?v=5194393";
    const imgurl2 = imgurl.toLowerCase();

    console.log(imgurl);
    return (
        
        <div className ="card">
            <div className = "imgstyle">
            <img src={imgurl2}  alt="icon" width='50px' borderRadius='10px' vspace="10px"></img>
            </div>
            <div className="namecenter">
            <b>{props.hero.name}</b> 
            </div>
           
            <div className ="container">
                <div className="inner">
                    <div className = "child">
                        
                        <p>{props.hero.type1} /{props.hero.type2}</p>
                        <p> HP: {props.hero.Health} </p>

                    </div>
                    <div className = "child">
                    <p>DPS: {props.hero.DPS}</p> 
                        <p>Range: {props.hero.Attack_Range}</p>
                        <p> Armor: {props.hero.Armor} </p>

                    </div>
                </div>
            </div>
            
            
            
            
            
            
        </div>

    )
}
export default Hero


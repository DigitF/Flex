import React from "react";
import "./css/flex.css"
import Header from './Header'


class Flex extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            view : "none"
        };
    }

    body(){
        if(this.state.view != "none") {
            return(
                <this.state.view />
            )
        } else {
            
        }
    }

    render() {
        return(
            <Header />
        )
    }
}

export default Flex
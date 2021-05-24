import React from "react";
import "./css/flex.css"
import Header from './Header'
import Movie from './Movie'


class Flex extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            searchValue : "",
            view : "none",
            params : []
        };
        this.body = this.body.bind(this);
        this.handleCardClick = this.handleCardClick.bind(this)
    }

    containers = {
        movie: Movie
    };

    body(){
        console.log("view : "+this.state.view)
        console.log("saerch : "+this.state.searchValue)
        const Container = this.containers[this.state.view];
        if(this.state.view != "none") {
            return(
                <div className="flex-container">
                    <Header searchValue={this.state.searchValue} clickHandler={this.handleCardClick}/>
                    <Container />
                </div>
            )
        } else {
            return(
                <div className="flex-container">
                    <Header searchValue={this.state.searchValue} clickHandler={this.handleCardClick}/>
                </div>
            )
        }
    }

    handleCardClick(props){
        console.log("set movie")
        this.setState({searchValue : "", view : "movie", title : props.title, genre : props.genre, overview : props.overview, poster : props.poster, firstAir : props.firstAir})
        
    }

    render() {
        console.log("rendering")
        return(
            <this.body />
        )
    };
}

export default Flex
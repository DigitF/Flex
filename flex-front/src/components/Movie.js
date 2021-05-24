import React from "react";
import "./css/movie.css"

class Movie extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            title = "",
            genre = "",
            overview = "",
            poster = "",
            firstAir = "",
            torrents = []
        }
    }

    render() {
        return(
            <div className="movie-view">
                <div className="head">
                    <div className="image-container">
                        <img src={"https://image.tmdb.org/t/p/w500" + this.state.poster} />
                    </div>
                    <div className="title-container">
                        <h1 className="title">{this.state.title}</h1>
                    </div>
                    <div className="buttons-container">
                        <i class="gg-search"></i> 
                        <i class="gg-add"></i>
                    </div>
                    
                </div>
            </div>
        )
    }
}
import React from "react";
import "./css/header.css"

class Header extends React.Component {

    constructor(props) {
        console.log("header : "+props.searchValue)
        super(props);
        this.state = {
            parentState: props.state,
            value: props.searchValue,
            cards: []
        };
        this.handleChange = this.handleChange.bind(this);
        this.initSearch = this.initSearch.bind(this);
        this.search = this.search.bind(this);
        this.showSuggetions = this.showSuggetions.bind(this);
        this.inputSearch = this.inputSearch.bind(this);
        this.card = this.card.bind(this);
    }

    handleChange(e) {
        this.setState({value : e.target.value})
        fetch("http://127.0.0.1:5000/autocomplete/?string="+ this.state.value, {
            crossDomain:true,
            method: 'GET'
        })
        .then(response => {
            response.json().then(json => {
                this.setState({cards : json})
            })
        })
    }

    initSearch(){
        return (
            <div className="header">
                <this.inputSearch />
            </div>
        )
    }

    inputSearch(){
        return (
            <input type="text" className="searchbar" onChange={this.handleChange} value={this.state.value} autoFocus="true"/>
        )
    }

    search(props){
        console.log("rendering hearder serach : "+props.value)
        if (props.value || props.value != "") {
            return( <this.showSuggetions /> )
        } else {
            return( <this.initSearch /> )
        }
    }

    card(params){
        return (
            <div className="card" onClick={this.props.clickHandler}>
                <img className="card-left" src={"https://image.tmdb.org/t/p/w200" + params.json.Poster} />
                <div className="card-right">
                    <div className="card-head">
                        <div className="card-title">
                            <h3>{params.json.Title}</h3>
                        </div>
                        <div className="card-buttons">
                            <i className="gg-search"></i> 
                            <i className="gg-add"></i>
                        </div>                     
                    </div>
                    <div className="card-overview">
                        <p>{params.json.Overview}</p>
                    </div>
                </div>
            </div>
        )
    }

    showSuggetions(){
        const cards = [];
        for (let card in this.state.cards) {
            cards.push(<this.card json={this.state.cards[card]}/>)
        }
        return (
            <div className="header">
                <this.inputSearch />
                <div className="suggestions">
                    {cards}
                </div>
            </div>
        )
    }

    render() {
        console.log("rendering header :" + this.state.value)
        return(
            <this.search value={this.state.value}/>
        )
    };
}

export default Header
import React, {Component} from "react";
import {Link} from "react-router-dom";

export class TestListItem extends Component {
    render() {
        return (
            <Link to={`/tests/${this.props.hash}`}>{this.props.title}</Link>
        );
    }
}


export default TestListItem;
import React, {Component} from "react";
import {connect} from "react-redux";
import * as ui from "semantic-ui-react";

import rest from "../rest";
import TestListItem from "./TestListItem"

const mapStateToProps = state => {
    return {api_tests: state.api_tests};
};

class ConnectedTestsList extends Component {
    componentDidMount() {
        rest.actions.api_tests.abort();
        this.props.dispatch(rest.actions.api_tests.list(this.props.page));
    }

    render() {
        return (
            <ui.Card.Group className="link" style={{justifyContent: "space-between"}}>
                {this.props.api_tests.data.map(test => <TestListItem {...test} key={test.id}/>)}
            </ui.Card.Group>
        );
    }
}

ConnectedTestsList.defaultProps = {
    page: 1
};

const TestsList = connect(mapStateToProps)(ConnectedTestsList);

export default TestsList;
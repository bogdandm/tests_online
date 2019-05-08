import React, {Component} from "react";
import {connect} from "react-redux";
import rest from "../../rest";

import {Test} from "./Test"

const mapStateToProps = state => {
    return {tests: state.tests};
};

export class ConnectedTestsList extends Component {
    componentDidMount() {
        this.props.dispatch(rest.actions.tests.list());
    }

    render() {
        return (
            <ul>
                {this.props.tests.data.map(
                    test => <Test key={test.id} {...test} />)
                }
            </ul>
        );
    }
}

const TestsList = connect(mapStateToProps)(ConnectedTestsList);

export default TestsList;
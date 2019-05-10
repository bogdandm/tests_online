import React, {Component} from "react";
import {connect} from "react-redux";
import * as ui from "semantic-ui-react";

import rest from "../rest";
import {TestListItem} from "./TestListItem"

const mapStateToProps = state => {
    return {tests: state.tests};
};

export class ConnectedTestsList extends Component {
    componentDidMount() {
        this.props.dispatch(rest.actions.tests.list());
    }

    render() {
        return (
            <ui.List divided relaxed>
                {this.props.tests.data.map(
                    test => <TestListItem key={test.id} {...test} />)
                }
            </ui.List>
        );
    }
}

const TestsList = connect(mapStateToProps)(ConnectedTestsList);

export default TestsList;
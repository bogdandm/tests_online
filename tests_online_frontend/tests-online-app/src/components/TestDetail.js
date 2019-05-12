import _ from "lodash";
import React, {Component} from "react";
import {connect} from "react-redux";
import * as ui from "semantic-ui-react";

import rest from "../rest";

const mapStateToProps = state => {
    return {...state.api_test};
};

class ConnectedTestDetail extends Component {
    componentDidMount() {
        this.props.dispatch(rest.actions.api_test.retrieve(this.props.match.params.hash));
    }

    render() {
        return (
            <ui.List.Item key={_.get(this.props, "data.id", null)}>
                <ui.List.Content>
                    <ui.List.Header>{_.get(this.props, "data.title", "")}</ui.List.Header>
                    <ui.List.Description>{_.get(this.props, "data.description", "")}</ui.List.Description>
                </ui.List.Content>
            </ui.List.Item>
        );
    }
}


export default connect(mapStateToProps)(ConnectedTestDetail);
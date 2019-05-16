import _ from "lodash";
import React, {Component} from "react";
import {connect} from "react-redux";
import * as ui from "semantic-ui-react";

import rest from "../rest";
import styles from "./ResultComponent.module.css"

const mapStateToProps = state => {
    return {...state.api_test_results};
};

class ConnectedResultComponent extends Component {
    componentDidMount() {
        this.props.dispatch(rest.actions.api_test_results.reset());
        this.props.dispatch(rest.actions.api_test_results.retrieve(this.props.test_hash));
    }

    render() {
        return <div className={styles.main}>
            <ui.Header as='h4'>Test complete!</ui.Header>
            {!_.isEmpty(_.get(this.props.data, 'bounds')) ?
                <div>
                    Your scores:<br/>
                    <ul>
                        {_.chain(this.props).get('data.bounds', {}).keys().value().map((key) =>
                            <li key={key}>
                                {key} [from {this.props.data.bounds[key][0]} to {this.props.data.bounds[key][1]}]:&nbsp;
                                {this.props.data.results[key]}
                            </li>
                        )}
                    </ul>
                </div>
                :
                <ui.Placeholder.Paragraph>
                    <ui.Placeholder.Line/>
                    <ui.Placeholder.Line/>
                    <ui.Placeholder.Line/>
                    <ui.Placeholder.Line/>
                </ui.Placeholder.Paragraph>
            }
        </div>
    }
}

export default connect(mapStateToProps)(ConnectedResultComponent);
import _ from "lodash";
import React, {Component} from "react";
import {connect} from "react-redux";
import {withRouter} from "react-router";
import * as ui from "semantic-ui-react";

import rest from "../rest";
import TestListItem from "./TestListItem"
import styles from "./TestsList.module.css"

const mapStateToProps = state => {
    return {api_tests: state.api_tests};
};

const PAGE_SIZE = 12;

class ConnectedTestsList extends Component {
    state = {
        page: this.props.page
    };

    componentDidMount() {
        rest.actions.api_tests.abort();
        this.loadPage();
    }

    loadPage(page = null) {
        if (_.isNull(page))
            page = this.state.page;
        this.props.dispatch(rest.actions.api_tests.list(page, PAGE_SIZE));
    }

    handlePaginationChange = (e, {activePage}) => {
        this.setState({page: activePage});
        this.props.history.push(`/tests/${activePage}`);
        this.loadPage(activePage);
    };

    render() {
        return (
            <div className={styles.wrapper}>
                <ui.Card.Group className="link" style={{justifyContent: "space-between"}}>
                    {_.isEmpty(this.props.api_tests.data) ?
                        [
                            _.range(5).map(() =>
                                <ui.Card>
                                    <ui.Card.Content>
                                        <ui.Card.Header style={{marginBottom: "1em"}}>
                                            <ui.Placeholder>
                                                <ui.Placeholder.Header>
                                                    <ui.Placeholder.Line/>
                                                </ui.Placeholder.Header>
                                            </ui.Placeholder>
                                        </ui.Card.Header>
                                        <ui.Card.Description>
                                            <ui.Placeholder>
                                                <ui.Placeholder.Paragraph>
                                                    <ui.Placeholder.Line/>
                                                    <ui.Placeholder.Line/>
                                                    <ui.Placeholder.Line/>
                                                    <ui.Placeholder.Line/>
                                                    <ui.Placeholder.Line/>
                                                    <ui.Placeholder.Line/>
                                                </ui.Placeholder.Paragraph>
                                            </ui.Placeholder>
                                        </ui.Card.Description>
                                    </ui.Card.Content>
                                </ui.Card>
                            ),
                            <div className="ui card" style={{opacity: 0}}/>
                        ]
                        :
                        [
                            _.get(this.props.api_tests.data, 'results', []).map(test =>
                                <TestListItem {...test} key={test.id}/>
                            ),
                            this.props.api_tests.data.results.length % 2 ?
                                <div className="ui card" style={{opacity: 0}}/> : ""
                        ]
                    }
                </ui.Card.Group>
                <ui.Pagination
                    defaultActivePage={this.state.page}
                    totalPages={_.get(this.props.api_tests.data, 'count', 1) / PAGE_SIZE}
                    onPageChange={this.handlePaginationChange}

                    ellipsisItem={{content: <ui.Icon name='ellipsis horizontal'/>, icon: true}}
                    firstItem={{content: <ui.Icon name='angle double left'/>, icon: true}}
                    lastItem={{content: <ui.Icon name='angle double right'/>, icon: true}}
                    prevItem={{content: <ui.Icon name='angle left'/>, icon: true}}
                    nextItem={{content: <ui.Icon name='angle right'/>, icon: true}}
                    style={{
                        marginTop: "2em"
                    }}
                />
            </div>
        );
    }
}

ConnectedTestsList.defaultProps = {
    page: 1
};

const TestsList = withRouter(connect(mapStateToProps)(ConnectedTestsList));

export default TestsList;
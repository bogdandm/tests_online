import _ from "lodash";
import React, {Component} from "react";
import {connect} from "react-redux";
import {withRouter} from "react-router";
import * as ui from "semantic-ui-react";

import rest from "../rest";
import QuestionComponent from "./QuestionComponent";
import ResultComponent from "./ResultComponent";
import styles from "./TestDetail.module.css"


const mapStateToProps = state => {
    return {test: state.api_test};
};

class ConnectedTestDetail extends Component {
    state = {
        questionIndex: this.props.questionIndex || 0,
        forceQuestionView: false
    };

    componentDidMount() {
        this.props.dispatch(rest.actions.api_test.reset());
        this.props.dispatch(rest.actions.api_test.retrieve(this.props.match.params.hash));
    }

    prevQuestion = () => {
        let newIndex = Math.max(0, this.state.questionIndex - 1);
        this.setState({questionIndex: newIndex});
        this.props.history.push(`/test/${this.props.match.params.hash}/${newIndex + 1}`);
    };

    nextQuestion = () => {
        let newIndex = Math.min(this.state.questionIndex + 1, this.props.test.data.questions.length);
        this.setState({questionIndex: newIndex});
        this.props.history.push(`/test/${this.props.match.params.hash}/${newIndex + 1}`);
    };

    setForceQuestionView = () => {
        this.setState({forceQuestionView: true})
    };

    unsetForceQuestionView = () => {
        this.setState({forceQuestionView: false})
    };

    render() {
        let data = this.props.test.data;
        let btnVisibilityClass = _.get(data, 'questions.length') === _.get(data, 'user_answers') ?
            " " + styles.hidden : "";

        return (
            <div className={styles.wrapper} id={`TestDetail_${this.props.match.params.hash}`}>
                <ui.Segment raised className={styles.card}>
                    <div className={styles.cardContainer}>
                        {_.isEmpty(data) ?
                            <ui.Placeholder>
                                <ui.Placeholder.Header>
                                    <ui.Placeholder.Line/>
                                </ui.Placeholder.Header>
                                <ui.Placeholder.Paragraph>
                                    <ui.Placeholder.Line/>
                                    <ui.Placeholder.Line/>
                                    <ui.Placeholder.Line/>
                                    <ui.Placeholder.Line/>
                                </ui.Placeholder.Paragraph>
                            </ui.Placeholder>
                            :
                            <div>
                                <ui.Header>{data.title}</ui.Header>
                                {data.description}
                            </div>
                        }
                    </div>
                    <ui.Divider horizontal>
                        Questions
                        ({this.state.questionIndex + 1}/{_.get(this, 'props.test.data.questions.length', '?')})
                    </ui.Divider>
                    <div className={styles.bottom}>
                        <div className={styles.buttonWrapperLeft + btnVisibilityClass}
                             disabled={this.state.questionIndex === 0}
                             onClick={this.prevQuestion}
                        >
                            <ui.Icon name="angle left"/>
                        </div>
                        <div className={styles.questionWrapper}>
                            {
                                _.isEmpty(data) ?
                                    <QuestionComponent
                                        test_hash={this.props.match.params.hash}
                                        key={null}
                                        qid={undefined}
                                    />
                                    :
                                    !this.state.forceQuestionView && data.questions.length === data.user_answers ?
                                        <div className={styles.questionWrapperInside}>
                                            <ResultComponent test_hash={this.props.match.params.hash}/>
                                            <ui.Button style={{alignSelf: "center"}}
                                                       onClick={this.setForceQuestionView}>
                                                Change answers
                                            </ui.Button>
                                        </div>
                                        :
                                        <div className={styles.questionWrapperInside}>
                                            <QuestionComponent
                                                test_hash={this.props.match.params.hash}
                                                key={"QuestionComponent#" + data.questions[this.state.questionIndex]}
                                                qid={data.questions[this.state.questionIndex]}
                                            />
                                            {this.state.forceQuestionView ?
                                                <ui.Button style={{alignSelf: "center"}}
                                                           onClick={this.unsetForceQuestionView}>
                                                    View results
                                                </ui.Button> : ""}
                                        </div>
                            }
                        </div>
                        <div className={styles.buttonWrapperRight + btnVisibilityClass}
                             disabled={_.isEmpty(data) || this.state.questionIndex + 1 === data.questions.length}
                             onClick={this.nextQuestion}
                        >
                            <ui.Icon name="angle right"/>
                        </div>
                    </div>
                </ui.Segment>
            </div>
        );
    }
}

export default withRouter(connect(mapStateToProps)(ConnectedTestDetail));
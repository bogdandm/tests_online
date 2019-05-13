import _ from "lodash";
import React, {Component} from "react";
import {connect} from "react-redux";
import {withRouter} from "react-router";
import * as ui from "semantic-ui-react";

import rest from "../rest";
import styles from "./TestDetail.module.css"


// ========================================================

const mapStateToProps = state => {
    return {test: state.api_test};
};

class ConnectedTestDetail extends Component {
    state = {
        questionIndex: 0
    };

    componentDidMount() {
        this.props.dispatch(rest.actions.api_test.reset());
        this.props.dispatch(rest.actions.api_test.retrieve(this.props.match.params.hash));
        if (!_.isEmpty(this.props.questionIndex))
            this.setState({questionIndex: this.props.questionIndex});
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

    render() {
        return (
            <div className={styles.wrapper}>
                <ui.Segment raised className={styles.card}>
                    <div className={styles.cardContainer}>
                        {_.isEmpty(this.props.test.data) ?
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
                                <ui.Header>{this.props.test.data.title}</ui.Header>
                                {this.props.test.data.description}
                            </div>
                        }
                    </div>
                    <ui.Divider horizontal>Questions</ui.Divider>
                    <div className={styles.bottom}>
                        <div className={styles.buttonWrapperLeft}
                             disabled={this.state.questionIndex === 0}
                             onClick={this.prevQuestion}
                        >
                            <ui.Icon name="angle left"/>
                        </div>
                        <div className={styles.questionWrapper}>
                            {
                                _.isEmpty(this.props.test.data) ?
                                    <QuestionComponent
                                        test_hash={this.props.match.params.hash}
                                        key={null}
                                    />
                                    :
                                    <QuestionComponent
                                        test_hash={this.props.match.params.hash}
                                        key={"QuestionComponent#" + this.props.test.data.questions[this.state.questionIndex]}
                                        qid={this.props.test.data.questions[this.state.questionIndex]}
                                    />
                            }
                        </div>
                        <div className={styles.buttonWrapperRight}
                             disabled={
                                 _.isEmpty(this.props.test.data)
                                 || this.state.questionIndex + 1 === this.props.test.data.questions.length
                             }
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


// ========================================================


const mapStateToPropsQuestion = state => {
    return {...state.api_question};
};

class ConnectedQuestionComponent extends Component {
    componentDidMount() {
        this.props.dispatch(rest.actions.api_question.reset());
        if (this.props.qid !== undefined)
            this.props.dispatch(rest.actions.api_question.retrieve(
                this.props.test_hash,
                this.props.qid
            ));
    }

    render() {
        return <ui.Transition.Group animation="fade" duration="500">
            {_.isEmpty(this.props.data) ?
                <ui.Placeholder>
                    <ui.Placeholder.Paragraph>
                        <ui.Placeholder.Line/>
                        <ui.Placeholder.Line/>
                        <ui.Placeholder.Line/>
                        <ui.Placeholder.Line/>
                    </ui.Placeholder.Paragraph>
                </ui.Placeholder>
                :
                <div>
                    {this.props.data.text}
                    <ui.Divider/>
                    {this.props.data.answers.map((answer) =>
                        <div key={answer.id}>
                            {answer.text}
                        </div>
                    )}
                    <ui.Divider/>
                    <ui.Button>Reset</ui.Button>
                </div>
            }
        </ui.Transition.Group>
    }
}

const QuestionComponent = connect(mapStateToPropsQuestion)(ConnectedQuestionComponent);
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
        if (this.props.questionIndex !== undefined)
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

// TODO: Disable answers for anon user
class ConnectedQuestionComponent extends Component {
    componentDidMount() {
        this.props.dispatch(rest.actions.api_question.reset());
        if (this.props.qid !== undefined)
            this.props.dispatch(rest.actions.api_question.retrieve(
                this.props.test_hash,
                this.props.qid
            ));
    }

    setAnswer = (e, {value}) => {
        this.syncAnswer(value)
    };

    resetAnswer = () => {
        this.syncAnswer(null)
    };

    syncAnswer(answer_id) {
        this.props.data.answers.forEach(answer => {
            answer.is_user_answer = answer.id === answer_id
        });
        if (answer_id !== null) {
            this.props.dispatch(rest.actions.api_give_answer.do(this.props.test_hash, this.props.qid, answer_id))
        } else {
            // TODO
        }
    }

    render() {
        return <ui.Transition.Group animation="fade" duration="500">
            {_.isEmpty(this.props.data) ?
                <div>
                    <ui.Placeholder>
                        <ui.Placeholder.Paragraph>
                            <ui.Placeholder.Line/>
                            <ui.Placeholder.Line/>
                            <ui.Placeholder.Line/>
                            <ui.Placeholder.Line/>
                        </ui.Placeholder.Paragraph>
                    </ui.Placeholder>
                    <ui.Divider/>
                    <ui.Placeholder>
                        {[0, 1, 2, 3].map((answer) =>
                            <ui.Placeholder.Paragraph key={answer}>
                                <ui.Placeholder.Line/>
                            </ui.Placeholder.Paragraph>
                        )}
                    </ui.Placeholder>
                </div>
                :
                <div>
                    {this.props.data.text}
                    <ui.Divider/>
                    {this.props.data.answers.map((answer) =>
                        <div key={answer.id}>
                            <ui.Checkbox
                                label={answer.text}
                                name='answersGroup'
                                value={answer.id}
                                checked={answer.is_user_answer}
                                onChange={this.setAnswer}
                            />
                        </div>
                    )}
                </div>
            }
            <ui.Divider/>
            <ui.Button onClick={this.resetAnswer}>Reset answer</ui.Button>
        </ui.Transition.Group>
    }
}

const QuestionComponent = connect(mapStateToPropsQuestion)(ConnectedQuestionComponent);
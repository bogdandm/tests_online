import _ from "lodash";
import React, {Component} from "react";
import {connect} from "react-redux";
import {async} from "redux-api";
import * as ui from "semantic-ui-react";

import rest from "../rest";

const mapStateToProps = state => {
    return {
        authorized: _.chain(state).get('api_user_info.data.id', null).isNumber().value(),
        ...state.api_question
    };
};

class ConnectedQuestionComponent extends Component {
    state = {
        synchronizing: false
    };

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

    syncAnswer(answer_id) {
        this.props.data.answers.forEach(answer => {
            answer.is_user_answer = answer.id === answer_id
        });
        this.setState({synchronizing: true});
        async(
            this.props.dispatch,
            cb => rest.actions.api_give_answer.do(this.props.test_hash, this.props.qid, answer_id, cb)
        )
            .then(() => this.setState({synchronizing: false}))
            .then(() => this.props.dispatch(rest.actions.api_test.retrieve(this.props.test_hash)));
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
                    <p style={{textAlign: "justify"}}>{this.props.data.text}</p>
                    <ui.Divider/>
                    {this.props.authorized ?
                        this.props.data.answers.map((answer) =>
                            <div key={answer.id} style={{marginBottom: "1em"}}>
                                {this.state.synchronizing && answer.is_user_answer ?
                                    <div>
                                        <ui.Loader size="tiny" active inline style={{marginRight: "1em"}}/>
                                        <span>{answer.text}</span>
                                    </div>
                                    :
                                    <ui.Checkbox
                                        label={answer.text}
                                        name='answersGroup'
                                        value={answer.id}
                                        checked={answer.is_user_answer}
                                        disabled={answer.is_user_answer}
                                        onChange={this.setAnswer}
                                    />
                                }
                            </div>
                        )
                        :
                        <ul>
                            {this.props.data.answers.map((answer) =>
                                <li key={answer.id} style={{textAlign: "justify"}}>
                                    {answer.text}
                                </li>
                            )}
                        </ul>
                    }
                </div>
            }
        </ui.Transition.Group>
    }
}

export default connect(mapStateToProps)(ConnectedQuestionComponent);
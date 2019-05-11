import _ from "lodash";
import React, {Component} from "react";
import {connect} from "react-redux";
import {Control, Errors, Form} from "react-redux-form";
import * as ui from "semantic-ui-react";

import rest from "../rest";


class ApiErrors extends Component {
    render() {
        if (this.props.error === null || this.props.error === undefined) return null;
        return _.get(this.props.error.response.data, this.props.field, [])
            .map((msg) => <ui.Message error content={msg}/>);
    }
}


const mapStateToProps = state => {
    return {auth: state.auth, api_user_signup: state.api_user_signup, ...state.forms.signup};
};

class ConnectedSignupForm extends Component {
    handleSubmit(data) {
        this.props.dispatch(rest.actions.api_user_signup({}, {
            data: {
                username: data.username,
                email: data.email,
                password: data.password,
            }
        }));
    }

    componentWillUnmount() {
        this.props.onClose()
    }

    render() {
        return (
            <ui.TransitionablePortal open={this.props.open} transition={{
                animation: "fade down",
                duration: 300
            }}>
                <ui.Modal open={true} onClose={this.props.onClose}>
                    <ui.Modal.Header>Signup</ui.Modal.Header>
                    <ui.Modal.Content>
                        <ui.Modal.Description>
                            <div style={{display: 'none'}}>
                                {_.get(this.props.api_user_signup.error, 'response.data.password.0')}
                            </div>
                            <Form
                                model="forms.signup"
                                onSubmit={(data) => this.handleSubmit(data)}
                                component={ui.Form}
                                validators={{
                                    '': {passwordsMatch: (data) => data.password === data.password2}
                                }}
                                error
                            >
                                <ui.Form.Field>
                                    <label htmlFor="signup.username">Username:</label>
                                    <Control.text model=".username" id="signup.username"
                                                  component={ui.Input} placeholder="Username" required/>
                                </ui.Form.Field>
                                <ApiErrors error={this.props.api_user_signup.error} field="username"/>

                                <ui.Form.Field>
                                    <label htmlFor="signup.email">Email:</label>
                                    <Control.text model=".email" id="signup.email"
                                                  component={ui.Input} placeholder="Email" required/>
                                </ui.Form.Field>
                                <ApiErrors error={this.props.api_user_signup.error} field="email"/>

                                <ui.Form.Field>
                                    <label htmlFor="signup.password">Password:</label>
                                    <Control.input type="password" model=".password" id="signup.password"
                                                   component={ui.Input} placeholder="Password" required/>
                                </ui.Form.Field>
                                <ApiErrors error={this.props.api_user_signup.error} field="password"/>

                                <ui.Form.Field>
                                    <label htmlFor="signup.password2">Repeat password:</label>
                                    <Control.input type="password" model=".password2" id="signup.password2"
                                                   component={ui.Input} placeholder="Repeat password"/>
                                </ui.Form.Field>

                                <Errors
                                    model="forms.signup"
                                    messages={{
                                        passwordsMatch: 'Passwords do not match.',
                                    }}
                                    component={(props) => <ui.Message error content={props.children}/>}
                                    show="touched"
                                />

                                <ui.Button type='button' disabled style={{transform: "scale(0)"}}>-</ui.Button>
                                <ui.Button type='submit' floated="right" primary
                                           loading={this.props.api_user_signup.loading}>
                                    Signup
                                </ui.Button>

                            </Form>
                        </ui.Modal.Description>
                    </ui.Modal.Content>
                </ui.Modal>
            </ui.TransitionablePortal>
        )
    }
}

const SignupForm = connect(mapStateToProps)(ConnectedSignupForm);

export default SignupForm;
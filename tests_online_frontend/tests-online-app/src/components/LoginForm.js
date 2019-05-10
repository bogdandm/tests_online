import React, {Component} from "react";
import {connect} from "react-redux";
import {Control, Form} from "react-redux-form";
import * as ui from "semantic-ui-react";


import rest from "../rest";


const mapStateToProps = state => {
    return {auth: state.auth, ...state.forms.user};
};


class ConnectedLoginForm extends Component {
    handleSubmit(user) {
        this.props.dispatch(rest.actions.auth.obtain(
            user.username, user.password
        ));
    }

    render() {
        return (
            <ui.TransitionablePortal open={this.props.open} transition={{
                animation: "fade down",
                duration: 300
            }}>
                <ui.Modal open={true} onClose={this.props.onClose}>
                    <ui.Modal.Header>Log in</ui.Modal.Header>
                    <ui.Modal.Content>
                        <ui.Modal.Description>
                            <Form
                                model="forms.user"
                                onSubmit={(user) => this.handleSubmit(user)}
                                component={ui.Form}
                            >
                                <ui.Form.Field>
                                    <label htmlFor="user.username">Username:</label>
                                    <Control.text model=".username" id="user.username"
                                                  component={ui.Input} placeholder="Username"/>
                                </ui.Form.Field>
                                <ui.Form.Field>
                                    <label htmlFor="user.password">Password:</label>
                                    <Control.input type="password" model=".password" id="user.password"
                                                   component={ui.Input} placeholder="Password"/>
                                </ui.Form.Field>
                                <ui.Button type='button' disabled style={{transform: "scale(0)"}}>-</ui.Button>
                                <ui.Button type='submit' floated="right" primary loading={this.props.auth.loading}>
                                    Log in
                                </ui.Button>
                            </Form>
                        </ui.Modal.Description>
                    </ui.Modal.Content>
                </ui.Modal>
            </ui.TransitionablePortal>
        )
    }
}

const LoginForm = connect(mapStateToProps)(ConnectedLoginForm);

export default LoginForm;
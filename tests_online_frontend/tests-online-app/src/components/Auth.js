import React, {Component} from "react";
import {connect} from "react-redux";
import {Control, Form,} from 'react-redux-form';


import rest from "../rest";


const mapStateToProps = state => {
    return {...state.auth, ...state.forms.user};
};


class ConnectedAuth extends Component {
    handleSubmit(user) {
        this.props.dispatch(rest.actions.test.list(
            user.username, user.password
        ));
    }

    render() {
        return (
            <div>
                <div>Access token: {this.props.data.access ? this.props.data.access.slice(0, 10) + "..." : ""}</div>
                <Form
                    model="forms.user"
                    onSubmit={(user) => this.handleSubmit(user)}
                >
                    <div>
                        <label htmlFor="user.username">Username:</label>
                        <Control.text model=".username" id="user.username"/>
                    </div>
                    <div>
                        <label htmlFor="user.password">Password:</label>
                        <Control.input type="password" model=".password" id="user.password"/>
                    </div>
                    <div>
                        <button type="submit">Log in</button>
                    </div>
                </Form>
            </div>
        )
    }
}

const Auth = connect(mapStateToProps)(ConnectedAuth);

export default Auth;
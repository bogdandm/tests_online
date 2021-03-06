import React, {Component} from "react";
import {connect} from "react-redux";
import * as ui from "semantic-ui-react";

import {creators} from "../actions";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";


const mapStateToProps = state => {
    return {auth: state.auth, user: state.api_user_info};
};

class ConnectedAuth extends Component {
    state = {open: null};

    componentDidMount() {
        this.props.dispatch(creators.auth.loadAndVerify())
    }

    handleLogout() {
        this.props.dispatch(creators.auth.logout())
    }

    openLoginForm = () => this.setState({open: "LoginForm"});
    openSignupForm = () => this.setState({open: "SignupForm"});
    closeAny = () => {
        this.setState({open: null});
    };

    render() {
        return this.props.auth.access ? (
            <ui.Dropdown item text={this.props.user.data.username} loading={!this.props.user.data.username}>
                <ui.Dropdown.Menu>
                    <ui.Dropdown.Item onClick={() => this.handleLogout()}>
                        Log out
                    </ui.Dropdown.Item>
                </ui.Dropdown.Menu>
            </ui.Dropdown>
        ) : (
            <ui.Menu.Menu position='right'>
                <ui.Menu.Item onClick={this.openLoginForm}>
                    Log in
                </ui.Menu.Item>
                <ui.Menu.Item onClick={this.openSignupForm}>
                    Signup
                </ui.Menu.Item>

                <LoginForm open={this.state.open === "LoginForm"} onClose={this.closeAny}/>
                <SignupForm open={this.state.open === "SignupForm"} onClose={this.closeAny}/>
            </ui.Menu.Menu>
        )
    }
}

const Auth = connect(mapStateToProps)(ConnectedAuth);

export default Auth;
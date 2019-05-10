import React, {Component} from "react";
import {connect} from "react-redux";
import * as ui from "semantic-ui-react";
import {creators} from "../actions";

import LoginForm from "./LoginForm";

const mapStateToProps = state => {
    return {auth: state.auth};
};


// TODO: username

class ConnectedAuth extends Component {
    state = {open: null};

    componentDidMount() {
        this.props.dispatch(creators.auth.loadAndVerify())
    }

    handleLogout() {
        this.props.dispatch(creators.auth.logout())
    }

    openLoginForm = () => this.setState({open: "LoginForm"});
    closeAny = () => this.setState({open: null});

    render() {
        return this.props.auth.data.access ? (
            <ui.Dropdown item text={"username"}>
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
                    <LoginForm open={this.state.open === "LoginForm"} onClose={this.closeAny}/>
                </ui.Menu.Item>
                <ui.Menu.Item onClick={null}>
                    Signup
                </ui.Menu.Item>
            </ui.Menu.Menu>
        )
    }
}

const Auth = connect(mapStateToProps)(ConnectedAuth);

export default Auth;
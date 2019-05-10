import React, {Component} from "react";
import {connect} from "react-redux";
import * as ui from "semantic-ui-react";
import LoginForm from "./LoginForm";

const mapStateToProps = state => {
    return {auth: state.auth};
};


// TODO: username

class ConnectedAuth extends Component {
    state = {open: null};

    openLoginForm = () => this.setState({open: "LoginForm"});
    closeAny = () => this.setState({open: null});

    render() {
        // noinspection ConstantConditionalExpressionJS
        return (
            true ? (
                <ui.Dropdown item text={"username"}>
                    <ui.Dropdown.Menu>
                        <ui.Dropdown.Item>
                            Log out
                        </ui.Dropdown.Item>
                    </ui.Dropdown.Menu>
                </ui.Dropdown>
            ) : (
                <ui.Menu.Item position="right">
                    <ui.Button.Group>
                        <ui.Button onClick={this.openLoginForm}>
                            Log in
                        </ui.Button>
                        <ui.Button primary>
                            Signup
                        </ui.Button>

                        <LoginForm open={this.state.open === "LoginForm"} onClose={this.closeAny}/>
                    </ui.Button.Group>
                </ui.Menu.Item>
            )
        )
    }
}

const Auth = connect(mapStateToProps)(ConnectedAuth);

export default Auth;
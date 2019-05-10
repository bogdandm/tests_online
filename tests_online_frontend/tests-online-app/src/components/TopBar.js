import React, {Component} from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import * as ui from "semantic-ui-react";

import Auth from "./Auth";


const mapStateToProps = state => {
    return state;
};

export class ConnectedTopBar extends Component {
    render() {
        return (
            <ui.Segment inverted>
                <ui.Menu fixed='top' inverted borderless>
                    <ui.Container>
                        <ui.Menu.Item header position="left">
                            <Link to="/" style={{fontSize: "120%"}}>
                                <span style={{fontSize: "150%"}}>Tests</span>
                                <span style={{opacity: .7}}>online</span>
                            </Link>
                        </ui.Menu.Item>
                        <Auth/>
                    </ui.Container>
                </ui.Menu>
            </ui.Segment>
        );
    }
}

const TopBar = connect(mapStateToProps)(ConnectedTopBar);

export default TopBar;
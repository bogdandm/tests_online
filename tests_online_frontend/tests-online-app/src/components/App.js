import React, {Component} from "react";
import {connect} from "react-redux";
import {Route} from "react-router";
import 'semantic-ui-css/semantic.min.css';
import * as ui from "semantic-ui-react";

import TestDetail from "./TestDetail";
import TestsList from "./TestsList";
import TopBar from "./TopBar";


const mapStateToProps = state => state;

export class ConnectedApp extends Component {
    render() {
        return (
            <div id="app-root">
                <TopBar/>
                <ui.Container key={"container" + this.props.uiKey}>
                    <Route exact path="/" component={TestsList}/>
                    <Route exact path="/tests" component={TestsList}/>
                    <Route path="/tests/:hash" component={TestDetail}/>
                </ui.Container>
            </div>
        );
    }
}

const App = connect(mapStateToProps)(ConnectedApp);

export default App;
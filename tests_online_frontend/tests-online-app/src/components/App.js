import React, {Component} from "react";
import {Route} from "react-router";
import 'semantic-ui-css/semantic.min.css';
import * as ui from "semantic-ui-react";

import TestDetail from "./TestDetail";
import TestsList from "./TestsList";
import TopBar from "./TopBar";

export class App extends Component {
    render() {
        return (
            <div id="app-root">
                <TopBar/>
                <ui.Container>
                    <Route exact path="/" component={TestsList}/>
                    <Route exact path="/tests" component={TestsList}/>
                    <Route path="/tests/:hash" component={TestDetail}/>
                </ui.Container>
            </div>
        );
    }
}

export default App;
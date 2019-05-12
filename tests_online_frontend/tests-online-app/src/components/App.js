import React, {Component} from "react";
import {connect} from "react-redux";
import {Route, Switch} from "react-router";
import 'semantic-ui-css/semantic.min.css';
import * as ui from "semantic-ui-react";

import TestDetail from "./TestDetail";
import TestsList from "./TestsList";
import TopBar from "./TopBar";


const mapStateToProps = state => state;

class ConnectedApp extends Component {
    render() {
        return (
            <div id="app-root">
                <TopBar/>
                <ui.Container key={"container" + this.props.uiKey} style={{marginTop: '7em'}}>
                    <Switch>
                        <Route exact path="/" component={TestsList}/>
                        <Route exact path="/tests" component={TestsList}/>
                        <Route path="/tests/:page" render={props =>
                            <TestsList {...props} page={props.match.params.page}/>
                        }/>
                        <Route path="/test/:hash" component={TestDetail}/>
                    </Switch>
                </ui.Container>
            </div>
        );
    }
}

const App = connect(mapStateToProps)(ConnectedApp);

export default App;
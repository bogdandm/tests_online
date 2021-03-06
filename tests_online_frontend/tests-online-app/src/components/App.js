import React, {Component} from "react";
import {connect} from "react-redux";
import {Route, Switch} from "react-router";
import 'semantic-ui-css/semantic.min.css';
// import 'semantic-forest/semantic.github.min.css';
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
                        <Route exact path="/" render={props => <TestsList {...props}/>}/>
                        <Route exact path="/tests" render={props => <TestsList {...props}/>}/>
                        <Route path="/tests/:page" render={props =>
                            <TestsList {...props} page={props.match.params.page}/>
                        }/>
                        <Route path="/test/:hash/:questionIndex" render={props =>
                            <TestDetail {...props} questionIndex={props.match.params.questionIndex - 1}/>
                        }/>
                        <Route path="/test/:hash" render={props => <TestDetail {...props}/>}/>
                    </Switch>
                </ui.Container>
            </div>
        );
    }
}

const App = connect(mapStateToProps)(ConnectedApp);

export default App;
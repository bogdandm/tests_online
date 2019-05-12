import React from "react"
import ReactDOM from "react-dom"
import {Provider} from "react-redux";
import {Router} from "react-router-dom";

import App from "./components/App";
import history from './history'
import * as serviceWorker from "./serviceWorker";
import store from "./store";
import './style.css'


ReactDOM.render(
    <Provider store={store}>
        <Router history={history}>
            <App/>
        </Router>
    </Provider>,
    document.getElementById('root')
);

serviceWorker.register();

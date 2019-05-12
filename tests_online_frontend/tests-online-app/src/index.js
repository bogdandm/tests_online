import React from "react"
import ReactDOM from "react-dom"
import {Provider} from "react-redux";
import {BrowserRouter} from "react-router-dom";

import App from "./components/App";
import * as serviceWorker from "./serviceWorker";
import store from "./store";
import './style.css'


ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter>
            <App/>
        </BrowserRouter>
    </Provider>,
    document.getElementById('root')
);

serviceWorker.register();

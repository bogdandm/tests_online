import React from "react"
import ReactDOM from "react-dom"
import {Provider} from "react-redux";
import {BrowserRouter} from "react-router-dom";
import {applyMiddleware, createStore} from "redux";
import thunk from "redux-thunk";

import App from "./components/App";
import reducer, {initialState} from "./reducers";

import * as serviceWorker from "./serviceWorker";


const store = createStore(reducer, initialState, applyMiddleware(thunk));
console.log("Store initial state: ", store.getState());

ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter>
            <App/>
        </BrowserRouter>
    </Provider>,
    document.getElementById('root')
);

serviceWorker.register();

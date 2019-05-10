import _ from "lodash";
import {combineForms} from "react-redux-form";
import {applyMiddleware, combineReducers, createStore} from "redux";
import logger from "redux-logger";
import thunk from "redux-thunk";

import {authGlobal, initialState, setRestInitialState} from "./reducers";
import rest from "./rest";

let store;


// TODO: Handle broken tokens
let restApi = rest.use("responseHandler", (err, response) => {
    if (err) {
        console.warn("API Error: ", err);
    } else {
        console.info("API response: ", response);
        return response.data
    }
});

const autoReducer = combineReducers({
    ...restApi.reducers,
    forms: combineForms({user: initialState.forms.user}, 'forms'),
    auth: (auth) => _.chain(auth).cloneDeep().defaults(initialState.auth).value()
});

function reducer(state, action) {
    return [state, autoReducer, authGlobal, setRestInitialState(initialState)].reduce((state, fn) => {
        return fn(state, action);
    });
}

store = createStore(reducer, initialState, applyMiddleware(thunk, logger));
console.log("Store initial state: ", store.getState());

export default store;
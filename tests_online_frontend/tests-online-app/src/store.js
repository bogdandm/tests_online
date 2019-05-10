import {combineForms} from "react-redux-form";
import {applyMiddleware, combineReducers, createStore} from "redux";
import logger from "redux-logger";
import thunk from "redux-thunk";

import {auth, initialState, setRestInitialState} from "./reducers";
import rest from "./rest";

let store;

let restApi = rest.use("responseHandler", (err, data) => {
    if (err) {
        console.warn("API Error: ", err);
    } else {
        console.info("API response: ", data);
        return data.data
    }
});

const autoReducer = combineReducers({
    ...restApi.reducers,
    forms: combineForms({user: initialState.forms.user}, 'forms')
});

function reducer(state, action) {
    return [state, autoReducer, auth, setRestInitialState(initialState)].reduce((state, fn) => {
        return fn(state, action);
    });
}

store = createStore(reducer, initialState, applyMiddleware(thunk, logger));
console.log("Store initial state: ", store.getState());

export default store;
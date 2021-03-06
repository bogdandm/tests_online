import cogoToast from 'cogo-toast';
import _ from "lodash";
import {combineForms} from "react-redux-form";
import {applyMiddleware, combineReducers, createStore} from "redux";
import {async} from "redux-api";
import logger from "redux-logger";
import thunk from "redux-thunk";

import {creators} from "./actions";
import {authGlobal, globalReducer, initialState, setRestInitialState} from "./reducers";
import rest, {requestsInProgress} from "./rest";

let store;
let restApi = rest.use("responseHandler", function (error, response) {
    const state = store.getState();

    if (error) {
        if (
            error.response.status === 401
            && error.response.data.code === "token_not_valid"
        ) {
            if (error.config.url.endsWith('/refresh/')) {
                store.dispatch(creators.auth.logout());
            } else {
                requestsInProgress
                    .filter(request => request.active)
                    .forEach(request => {
                        request.active = false;
                        console.warn(`Cancel request ${request.url}`);
                        request.source.cancel(request.url)
                    });
                async(
                    store.dispatch,
                    (cb) => {
                        return rest.actions.api_auth_refresh.refresh(state.auth.refresh, cb)
                    }
                ).then((data) => store.dispatch(creators.forceUpdate()));
            }
            throw error;
        } else {
            console.warn("API Error: ", error);
            if (process.env.NODE_ENV === "development")
                cogoToast.error(`${error.toString()}: ${error.config.method.toUpperCase()} ${error.config.url}`);
            throw error;
        }
    } else {
        console.info("API response: ", response);
        return response.data
    }
});

const autoReducer = combineReducers({
    ...restApi.reducers,
    forms: combineForms({
        user: initialState.forms.user,
        signup: initialState.forms.signup
    }, 'forms'),
    auth: (auth) => _.chain(auth).cloneDeep().defaults(initialState.auth).value(),
    uiKey: (key) => key || 1
});

function reducer(state, action) {
    return [
        state,
        autoReducer,
        authGlobal, globalReducer,
        setRestInitialState(initialState)
    ].reduce((state, fn) => {
        return fn(state, action);
    });
}

const middleware = process.env.NODE_ENV === "development" ? [thunk, logger] : [thunk];
store = createStore(reducer, initialState, applyMiddleware(...middleware));
console.log("Store initial state: ", store.getState());

export default store;
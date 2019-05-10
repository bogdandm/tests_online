import _ from "lodash";
import {combineForms} from "react-redux-form";
import {combineReducers} from "redux";

import {actions} from "./actions";
import rest, {stateAsyncFactory} from "./rest";


export const initialState = {
    auth: stateAsyncFactory({
        access: null,
        refresh: null
    }),
    tests: stateAsyncFactory([]),
    test: stateAsyncFactory(null),
    forms: {
        user: {
            username: '',
            password: ''
        }
    }
};

function setRestInitialState(initialState) {
    return (state) => {
        const newState = _.chain(state).defaults(initialState).cloneDeep().value();
        newState.tests.data = _.isEmpty(newState.tests.data) ? initialState.tests.data : newState.tests.data;
        return newState;
    }
}

function auth(state, action) {
    state = _.cloneDeep(state);
    switch (action.type) {
        case rest.events.auth.actionFetch:
            state.forms.user.password = "";
            return state;

        case rest.events.auth.actionSuccess:
            localStorage.setItem("AUTH", JSON.stringify(action.data));
            return state;

        case actions.auth.load:
            let authInit = localStorage.getItem("AUTH");
            if (authInit) {
                authInit = JSON.parse(authInit);
                state.auth.data = authInit;
            }
            return state;

        case actions.auth.logout:
            state.auth.data = initialState.auth.data;
            localStorage.removeItem("AUTH");
            return state;

        default:
            return state;
    }
}

const autoReducer = combineReducers({
    ...rest.reducers,
    forms: combineForms({user: initialState.forms.user}, 'forms')
});

function reducer(state, action) {
    return [state, autoReducer, auth, setRestInitialState(initialState)].reduce((state, fn) => {
        return fn(state, action);
    });
}

export default reducer;
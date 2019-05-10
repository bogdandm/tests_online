import _ from "lodash";

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

export function setRestInitialState(initialState) {
    return (state) => {
        const newState = _.chain(state).defaults(initialState).cloneDeep().value();
        newState.tests.data = _.isEmpty(newState.tests.data) ? initialState.tests.data : newState.tests.data;
        return newState;
    }
}

export function auth(state, action) {
    state = _.cloneDeep(state);
    switch (action.type) {
        case rest.events.auth.actionFetch:
            state.forms.user.password = "";
            return state;

        case rest.events.auth.actionSuccess:
            if (action.request.pathvars.action === "obtain")
                localStorage.setItem("AUTH", JSON.stringify(action.data));
            return state;

        case actions.auth.load:
            let authInit = localStorage.getItem("AUTH");
            if (authInit) {
                try {
                    authInit = JSON.parse(authInit);
                    state.auth.data = authInit;
                } catch (e) {
                    authInit = null;
                    localStorage.removeItem("AUTH")
                }
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

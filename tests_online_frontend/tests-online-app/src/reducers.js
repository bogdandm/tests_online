import _ from "lodash";

import {actions} from "./actions";
import rest, {stateAsyncFactory} from "./rest";


export const initialState = {
    auth: {
        access: null,
        refresh: null,
        username: "username"
    },

    api_auth: stateAsyncFactory({
        access: null,
        refresh: null
    }),
    api_tests: stateAsyncFactory([]),
    api_test: stateAsyncFactory(null),

    forms: {
        // TODO: Rename to LogIn
        user: {
            username: '',
            password: ''
        }
    }
};

export function setRestInitialState(initialState) {
    return (state) => {
        const newState = _.chain(state).defaults(initialState).cloneDeep().value();
        newState.api_tests.data = _.isEmpty(newState.api_tests.data)
            ? initialState.api_tests.data
            : newState.api_tests.data;
        return newState;
    }
}

export function authGlobal(state, action) {
    state = _.cloneDeep(state);
    switch (action.type) {
        case rest.events.api_auth.actionFetch:
            state.forms.user.password = "";
            return state;

        case rest.events.api_auth.actionSuccess:
            if (action.request.pathvars.action === "obtain") {
                localStorage.setItem("AUTH", JSON.stringify(action.data));
                state.auth = {...state.auth, ...action.data};
            }
            return state;

        case actions.auth.load:
            let authInit = localStorage.getItem("AUTH");
            if (authInit) {
                try {
                    authInit = JSON.parse(authInit);
                    state.auth = {...state.auth, ...authInit};
                } catch (e) {
                    authInit = null;
                    localStorage.removeItem("AUTH")
                }
            }
            return state;

        case actions.auth.logout:
            state.auth = initialState.auth;
            localStorage.removeItem("AUTH");
            return state;

        default:
            return state;
    }
}

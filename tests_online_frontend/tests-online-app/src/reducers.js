import _ from "lodash";

import {actions} from "./actions";
import history from './history'
import rest, {stateAsyncFactory} from "./rest";

export const initialState = {
    uiKey: 1,

    auth: {
        access: null,
        refresh: null,
        username: "username"
    },

    api_user_info: stateAsyncFactory({
        id: null,
        username: null,
        email: null
    }),
    api_user_signup: stateAsyncFactory({
        id: null,
        username: null,
        email: null
    }),
    api_tests: stateAsyncFactory([]),
    api_test: stateAsyncFactory(null),
    api_question: stateAsyncFactory(null),

    forms: {
        // TODO: Rename to LogIn
        user: {
            username: '',
            password: ''
        },
        signup: {
            email: '',
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
        case rest.events.api_auth_refresh.actionSuccess:
            switch (action.request.pathvars.action) {
                case "refresh":
                case "obtain":
                    localStorage.setItem("AUTH", JSON.stringify(action.data));
                    state.auth = {...state.auth, ...action.data};
                    return state;

                default:
                    return state;
            }

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

        case actions.auth.login:
            setTimeout(() => history.push('/'), 16);
            return state;

        case actions.auth.logout:
            state.auth = initialState.auth;
            state.api_user_info.data = initialState.api_user_info.data;
            localStorage.removeItem("AUTH");
            setTimeout(() => history.push('/'), 16);
            return state;

        default:
            return state;
    }
}

export function globalReducer(state, action) {
    state = _.cloneDeep(state);
    switch (action.type) {
        case actions.forceUpdate:
            state.uiKey++;
            return state;

        default:
            return state;
    }
}
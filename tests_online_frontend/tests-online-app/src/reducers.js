import _ from "lodash";
import {combineForms} from "react-redux-form";
import {combineReducers} from "redux";
import rest, {stateAsyncFactory} from "./rest";

export const initialState = {
    auth: stateAsyncFactory({
        access: null,
        refresh: null
    }),
    tests: stateAsyncFactory([]),
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

function authGlobal(state, action) {
    switch (action.type) {
        case rest.events.auth.actionFetch:
            console.log(action);
        // return {
        //     ...state,
        //     form: {
        //         ...state.form,
        //         password: null
        //     }
        // };

        default:
            return state;
    }
}

const autoReducer = combineReducers({
    ...rest.reducers,
    forms: combineForms({user: initialState.forms.user}, 'forms')
});

function reducer(state, action) {
    return [state, autoReducer, authGlobal, setRestInitialState(initialState)].reduce((state, fn) => {
        return fn(state, action);
    });
}

export default reducer;
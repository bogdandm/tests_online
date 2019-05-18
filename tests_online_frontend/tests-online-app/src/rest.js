import axios, {CancelToken} from "axios";
import _ from "lodash";
import reduxApi from "redux-api";
import {creators} from "./actions";

export const requestsInProgress = [];

function adapterAxios(url, options) {
    const request = {source: CancelToken.source(), active: true, url: url};
    requestsInProgress.push(request);
    return axios.request({url, cancelToken: request.source.token, ...options})
        .then(
            response => {
                request.active = false;
                return response
            },
            e => {
                request.active = false;
                if (axios.isCancel(e)) {
                    console.warn('Request canceled', e.message || "");
                } else {
                    throw e
                }
            }
        );
}

export function stateAsyncFactory(nested) {
    return {
        data: _.clone(nested),
        sync: false,    // State was update once
        syncing: false, // State syncing is in progress
        loading: false, // State updating is in progress
        error: null,    // response error
    }
}

function fetchUserInfo({actions, dispatch}) {
    dispatch(actions.api_user_info());
}


// TODO: Prefix
// ({data, actions, dispatch, getState, request}) => {...}
export default reduxApi({
    api_auth: {
        url: `/api/v1/auth/token/:action/`,
        helpers: {
            obtain(username, password) {
                return [
                    {action: "obtain"},
                    {
                        method: "POST",
                        data: {username, password}
                    }
                ]
            },
            verify(token) {
                return [
                    {action: "verify"},
                    {
                        method: "POST",
                        data: {token}
                    }
                ]
            }
        },
        postfetch: [
            fetchUserInfo,
            ({request, dispatch}) => {
                if (request.pathvars.action === "obtain")
                    dispatch(creators.auth.login())
            }
        ]
    },
    // Duplicate endpoint to prevent race condition in store
    api_auth_refresh: {
        url: `/api/v1/auth/token/:action/`,
        helpers: {
            refresh(token) {
                return [
                    {action: "refresh"},
                    {
                        method: "POST",
                        data: {refresh: token}
                    }
                ]
            }
        },
        postfetch: [fetchUserInfo]
    },
    api_user_signup: {
        url: `/api/v1/auth/user/signup/`,
        options: {
            method: "post"
        },
        postfetch: [
            ({actions, dispatch, request}) => {
                dispatch(actions.api_auth.obtain(request.params.data.username, request.params.data.password))
            }
        ]
    },
    api_user_info: `/api/v1/auth/user/info/`,
    api_tests: {
        url: `api/v1/tests/`,
        helpers: {
            list(page = 1, pageSize = 10) {
                return [
                    {},
                    {
                        method: "GET",
                        params: {page, size: pageSize}
                    }
                ]
            }
        }
    },
    api_test: {
        url: `api/v1/tests/:id/`,
        helpers: {
            retrieve(id) {
                return [
                    {id},
                    {
                        method: "GET"
                    }
                ]
            }
        }
    },
    api_test_results: {
        url: `api/v1/tests/:id/results/`,
        helpers: {
            retrieve(id) {
                return [
                    {id},
                    {
                        method: "GET"
                    }
                ]
            }
        }
    },
    api_question: {
        url: `api/v1/tests/:test_id/questions/:id/`,
        helpers: {
            retrieve(test_id, id) {
                return [
                    {test_id, id},
                    {
                        method: "GET"
                    }
                ]
            }
        }
    },
    api_give_answer: {
        url: `api/v1/tests/:test_id/questions/:question_id/answers/:answer_id/give/`,
        helpers: {
            do(test_id, question_id, answer_id) {
                return [
                    {test_id, question_id, answer_id},
                    {
                        method: "POST",
                        data: {}
                    }
                ]
            }
        }
    }
}, {prefix: "api."})
    .use("fetch", adapterAxios)
    .use("rootUrl", process.env.REACT_APP_DOMAIN || "http://localhost:8000")
    .use("options", (url, params, getState) => {
        const state = getState();
        return {
            headers: {
                'Accept': 'application/json',
                ...(state.auth.access ? {'Authorization': `Bearer ${state.auth.access}`} : {})
            }
        }
    });
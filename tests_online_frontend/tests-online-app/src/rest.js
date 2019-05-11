import axios from "axios";
import _ from "lodash";
import reduxApi from "redux-api";

function adapterAxios(url, options) {
    return axios.request({url, ...options});
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

const paginator = (data, prevData, action) => {
    data || (data = {"results": []});
    return data.results
};


function postAuth({data, actions, dispatch, getState, request}) {
    dispatch(actions.api_user_info());
}


// TODO: Prefix
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
        postfetch: [postAuth]
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
        postfetch: [postAuth]
    },
    api_user_info: `/api/v1/auth/user/info/`,
    api_user_signup: {
        url: `/api/v1/auth/user/signup/`,
        options: {
            method: "post"
        },
        postfetch: [
            ({data, actions, dispatch, getState, request}) => {
                dispatch(actions.api_auth.obtain(request.params.data.username, request.params.data.password))
            }
        ]
    },
    api_tests: {
        url: `api/v1/tests/`,
        helpers: {
            list(page = 1) {
                return [
                    {},
                    {
                        method: "GET",
                        params: {page}
                    }
                ]
            }
        },
        transformer: paginator
    },
    api_test: {
        url: `api/v1/tests/:id`,
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
    }
}, {prefix: "api."})
    .use("fetch", adapterAxios)
    .use("rootUrl", "http://localhost:8000")
    .use("options", (url, params, getState) => {
        const state = getState();
        return {
            headers: {
                'Accept': 'application/json',
                ...(state.auth.access ? {'Authorization': `Bearer ${state.auth.access}`} : {})
            }
        }
    });
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

export default reduxApi({
    auth: {
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
            }
        }
    },
    tests: {
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
        transformer: (data, prevData, action) => {
            data || (data = {"results": []});
            return data.results
        }
    },
    test: {
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
})
    .use("fetch", adapterAxios)
    .use("rootUrl", "http://localhost:8000")
    .use("options", (url, params, getState) => {
        const state = getState();
        return {
            'Accept': 'application/json',
            ...(state.auth.data.access ? {'Authorization': `Bearer ${state.auth.data.access}`} : {})
        }
    })
    .use("responseHandler", (err, data) => {
        if (err) {
            console.warn("API Error: ", err);
        } else {
            console.info("API response: ", data);
            return data.data
        }
    });
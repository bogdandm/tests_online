import rest from "./rest"

export const actions = {
    auth: {
        load: "AUTH_LOAD",
        logout: "AUTH_LOGOUT"
    }
};

const generateCreator = (action) => () => {
    return {type: action}
};

export const creators = {
    auth: {
        load: generateCreator(actions.auth.load),
        loadAndVerify: () => (dispatch, getState) => {
            dispatch({type: actions.auth.load});
            const accessToken = getState().auth.access;
            accessToken && dispatch(rest.actions.api_auth.verify(accessToken));
        },
        logout: generateCreator(actions.auth.logout)
    }
};

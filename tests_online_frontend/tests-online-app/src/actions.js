import rest from "./rest"

export const actions = {
    forceUpdate: "FORCE_UPDATE", // Force redraw of main app view (everything except TopBar)
    auth: {
        load: "AUTH_LOAD",
        logout: "AUTH_LOGOUT"
    }
};

const generateCreator = (action) => () => {
    return {type: action}
};

export const creators = {
    forceUpdate: generateCreator(actions.forceUpdate),
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

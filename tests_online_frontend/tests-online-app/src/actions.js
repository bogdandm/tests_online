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
        logout: generateCreator(actions.auth.logout)

    }
};

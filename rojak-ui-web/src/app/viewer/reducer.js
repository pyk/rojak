
const initialState = {
    access_token: '',
    profile: {},
};

export default (state = initialState, action) => {
    const { payload, type } = action;
    switch (type) {
    case 'LOGIN':
        return state;
    default:
        return state;
    }
};

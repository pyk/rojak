
export default (state = [], action) => {
    const { payload, type } = action;
    switch (type) {
    case 'LOAD_SENTIMENTS_SUCCESS':
        return state.concat(
            payload.sentiments
        );
    default:
        return state;
    }
};

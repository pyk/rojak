const mediaMockup = require('./media.json');

const initialState = mediaMockup.data;

export default (state = initialState, action) => {
    const { payload, type } = action;
    switch (type) {
    default:
        return state;
    }
};

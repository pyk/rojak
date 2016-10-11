const candidateMockup = require('./candidate.json');

const initialState = candidateMockup.data;

export default (state = initialState, action) => {
    const { payload, type } = action;
    switch (type) {
    default:
        return state;
    }
};

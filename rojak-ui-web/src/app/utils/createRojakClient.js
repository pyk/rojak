const axios = require('axios');

const createRojakClient = (endpoint) => {
    const getSentimentsOfCandidate = (candidateId) => axios
        .get(`${endpoint}/candidates/${candidateId}/media-sentiments`)
        .then(resp => resp.data);

    return {
        getSentimentsOfCandidate,
    };
};

module.exports = createRojakClient;

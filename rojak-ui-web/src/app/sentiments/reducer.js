
export default (sentiments = [], action) => {
    const { payload, type } = action;
    switch (type) {
    case 'SET_SENTIMENTS_OF_CANDIDATE_ID':
        return [...sentiments, ...payload.sentiments
            .filter(sentiment => !sentiments.find(s => s.id === sentiment.id
                && s.candidateId === payload.candidateId))
            .map(sentiment => Object.assign({}, sentiment, {
                candidateId: payload.candidateId,
            }))
        ];
    default:
        return sentiments;
    }
};

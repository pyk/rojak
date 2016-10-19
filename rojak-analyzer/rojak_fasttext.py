# Rojak using fastText model by Facebook AI Research team
# References:
# Enriching Word Vectors with Subword Information
#     (https://arxiv.org/pdf/1607.04606.pdf)
# Bag of Tricks for Efficient Text Classification
#     (https://arxiv.org/pdf/1607.01759.pdf)
import fasttext

class RojakFastTextWrapper:
    def train(self, input_file, output_file):
        # TODO: access label prefix info from create_training_data.py
        #       or create new sub-command to create training data
        fasttext.supervised(input_file, output_file,
            label_prefix='__LABEL__', dim=300,
            min_count=1, thread=2, silent=0)

    # Returned object should have 'predict_proba' method
    def load_model(self, model_file):
        return fasttext.load_model(model_file,
                label_prefix='__LABEL__')

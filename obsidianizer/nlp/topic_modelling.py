from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


def build_lda(x_train, num_of_topic=10):
    vec = CountVectorizer()
    transformed_x_train = vec.fit_transform(x_train)
    feature_names = vec.get_feature_names()

    lda = LatentDirichletAllocation(
        n_components=num_of_topic, max_iter=5, learning_method="online", random_state=0
    )
    lda.fit(transformed_x_train)

    return lda, vec, feature_names


def display_word_distribution(model, feature_names, n_word):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        words = []
        for i in topic.argsort()[: -n_word - 1 : -1]:
            words.append(feature_names[i])
        print(words)


# lda_model, vec, feature_names = build_lda(x_train)
# display_word_distribution(model=lda_model, feature_names=feature_names, n_word=5)

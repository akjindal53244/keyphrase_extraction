from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.metrics import euclidean_distances
from sklearn.cluster import KMeans
from scipy.spatial import distance
import numpy as np
from scipy.spatial.distance import cdist, pdist
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import cPickle
from scipy import sparse

possible_clusters = range(5, 500, 10)

ensembled_file = "../resources/data/social_text_tokenized_pos_ensemble_filtered_topic_kpminer"
ensembled_file_useful_f = open("../resources/data/social_text_tokenized_pos_ensemble_filtered_topic_kpminer_useful",
                               "w")
embedding_file = "/home/asjindal/Downloads/paragram_300_sl999/paragram_300_sl999.txt"
pickle_path = "/home/asjindal/data/embeddings_pkl/paragram-phrase_xxl.pkl"
feature_matrix_path = "../resources/data/social_text_ensemble_feature_matrix"


lines = open(ensembled_file, "r").readlines()
lines = [line.strip() for line in lines if len(line.strip()) > 0]
print "Total Non-empty lines in file: {}".format(len(lines))


def get_feature_matrix_tf_idf():
    # check for feature vec len
    feature_matrix = TfidfVectorizer(min_df=15).fit_transform(lines)
    return feature_matrix


def get_feature_matrix_embeddings():
    w2v = get_pickle()
    useful_lines = []
    print "pkl Loaded!"

    feature_matrix = np.zeros((len(lines), 300), dtype=np.float64)
    all_feature_vecs = []
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) > 0:
            phrases = line.split(" , ")
            words = [word.strip() for phrase in phrases for word in phrase.split(" ") if len(word) > 0]

            embeddings = [w2v[word] for word in words if word in w2v]
            if len(embeddings) >1:
                feature_matrix[i] = np.sum(embeddings, axis=0) / len(embeddings)
                all_feature_vecs.append(list(feature_matrix[i]))
                useful_lines.append(line)
            elif len(embeddings) == 1:
                # print line, phrases, words
                # print embeddings, embeddings[0]
                feature_matrix[i] = np.array(embeddings[0])
                all_feature_vecs.append(list(feature_matrix[i]))
                useful_lines.append(line)

    print "Total Non-empty lines + non-zeros vectors in file: {}".format(len(useful_lines))
    final_feature_matrix = np.array(all_feature_vecs)
    np.savetxt(feature_matrix_path, final_feature_matrix, fmt='%.3e')
    ensembled_file_useful_f.write("\n".join(useful_lines))
    return sparse.csr_matrix(final_feature_matrix)


def dump_paragram_embeddings():
    word_vectors = {}
    embedding_lines = open(os.path.join(embedding_file), "r").readlines()

    for i, line in enumerate(embedding_lines):
        sp = line.strip().split(" ")
        if i % 100000 == 0:
            print i
        word_vectors[sp[0]] = map(lambda x: float(x), sp[1:])

    print "Loaded!"
    dump_pickle(word_vectors, "/home/asjindal/data/embeddings_pkl/paragram_sl.pkl")
    print "Done!"


def get_pickle():
    data = cPickle.load(open(pickle_path, "rb"))
    return data


def dump_pickle(data, path):
    with open(path, "w") as f:
        cPickle.dump(data, f)


# get feature Matrix
# feature_matrix = get_feature_matrix_tf_idf()



def run_KMeans(k):
    print "starting KMeans for k = {}".format(k)
    km = KMeans(n_clusters=k).fit(feature_matrix)
    print "Done!"
    return km



def analyze_clusters_Elbow():
    # Run Kmeans for all possible values of clusters
    scores = [KM[i].score(feature_matrix) for i in range(len(KM))]
    print "Elbow scores"
    for i,(k, score) in enumerate(zip(possible_clusters, scores)):
        print "k:{}\t score:{}".format(k, score)
    #
    # list_centroids = [k.cluster_centers_ for k in KM]
    # list_labels = [k.labels_ for k in KM]
    #
    # D_k = [cdist(feature_matrix, cent, 'euclidean') for cent in list_centroids]
    # cIdx = [np.argmin(D, axis=1) for D in D_k]
    # dist = [np.min(D, axis=1) for D in D_k]
    # avgWithinSS = [sum(d) / feature_matrix.shape[0] for d in dist]
    #
    # # Total with-in sum of square
    # wcss = [sum(d ** 2) for d in dist]
    # tss = sum(pdist(feature_matrix) ** 2) / feature_matrix.shape[0]
    # bss = tss - wcss
    #
    # # elbow curve
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # print possible_clusters
    # print avgWithinSS
    #
    # ax.plot(possible_clusters, vgWithinSS, 'b*-')
    # plt.grid(True)
    # plt.xlabel('Number of clusters')
    # plt.ylabel('Average within-cluster sum of squares')
    # plt.title('Elbow for KMeans clustering')
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(possible_clusters, bss / tss * 100, 'b*-')
    # plt.grid(True)
    # plt.xlabel('Number of clusters')
    # plt.ylabel('Percentage of variance explained')
    # plt.title('Elbow for KMeans clustering')
    # plt.show()


def analyze_clusters_silhouette():
    for i in range(len(KM)):
        labels = KM[i].labels_
        centroids = KM[i].cluster_centers_

        sil_coeff = silhouette_score(feature_matrix, labels, metric='euclidean')
        print("For n_clusters={}, The Silhouette Coefficient is {}".format(possible_clusters[i], sil_coeff))


feature_matrix = get_feature_matrix_embeddings()
KM = [run_KMeans(k) for k in possible_clusters]

analyze_clusters_silhouette()
analyze_clusters_Elbow()
# dump_paragram_embeddings()
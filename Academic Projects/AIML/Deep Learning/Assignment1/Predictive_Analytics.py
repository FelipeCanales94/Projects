# -*- coding: utf-8 -*-
"""
Predicitve_Analytics.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.preprocessing import StandardScaler


def getEuclidDistance(one, two):
    return np.linalg.norm(one - two)

def getData(data):
    df = pd.read_csv(data)
    df = df.sample(frac=1)    # Randomize data

    # split data into 2 sets -> Training Set (80% of total data), Test Set (20 % of total data)

    num_rows = df.shape[0]      # Get total number of rows
    total_splitter = int(num_rows * .20)    # Get 20% of total number of rows

    total_test, total_train = df[:total_splitter], df[total_splitter:]

    # Set features and labels for each set and convert to np arrays

    X_train = total_train.iloc[:, :-1].rename_axis('ID').values
    y_train = total_train.iloc[:, 48:].rename_axis('ID').values

    X_test = total_test.iloc[:, :-1].rename_axis('ID').values
    y_test = total_test.iloc[:, 48:].rename_axis('ID').values

    train_scale = StandardScaler().fit(X_train)
    normal_xtrain = train_scale.transform(X_train)

    test_scale = StandardScaler().fit(X_test)
    normal_xtest = test_scale.transform(X_test)

    return normal_xtrain, y_train, normal_xtest, y_test


def Accuracy(y_true,y_pred):
    """
    :type y_true: numpy.ndarray
    :type y_pred: numpy.ndarray
    :rtype: float
   """

    ypred = list(y_pred)
    ytrue = list(y_true)
    right = 0
    for i in range(y_true.shape[0]):
        if ypred[i] == ytrue[i]:
            right += 1

    return (right/y_true.shape[0]) * 100

def Recall(y_true,y_pred):

    """
    :type y_true: numpy.ndarray
    :type y_pred: numpy.ndarray
    :rtype: float
    """
    # Formula = true positive * 100 /(true positive + false negative)
    true_positives = sum((y_true == 1) & (y_pred == 1))
    false_negatives = sum((y_true == 1) & (y_pred == 0))

    return float((true_positives * 100)/(true_positives + false_negatives))


def Precision(y_true,y_pred):
    """
    :type y_true: numpy.ndarray
    :type y_pred: numpy.ndarray
    :rtype: float
    """
    # Formula = true positive * 100 / (true positive + false positive)
    true_positives = sum((y_true == 1) & (y_pred == 1))     # true positive if both true and pred = 1
    false_positive = sum((y_true == 0) & (y_pred == 1))     # false positive if pred = 1 but actual = 0

    return float((true_positives * 100)/(true_positives + false_positive))


def WCSS(Clusters):
    """
    :Clusters List[numpy.ndarray]
    :rtype: float
    """
    # takes in list of arrays. length of list is number of clusters. each element in list contains rows of data corresponding to that cluster

    wccs_each = ([])
    for x in range(0, len(Clusters)):
        # formula
        wccs = float(np.sum(np.square(Clusters[x] - np.mean(Clusters[x]))))
        wccs_each.append(wccs)

    hold = np.array(wccs_each)
    ans = float(np.sum(np.square(hold - np.mean(hold))))

    return ans


def ConfusionMatrix(y_true, y_pred):
    
    """
    :type y_true: numpy.ndarray
    :type y_pred: numpy.ndarray
    :rtype: numpy.ndarray
    """

    classes = pd.DataFrame(y_test).nunique()      # number of unique classes
    matrix = np.zeros((classes.get(0), classes.get(0)))   # initialize matrix

    for x, y in zip(y_true, y_pred):    # iterate list
        matrix[x[0]-1][y-1] += 1   # create matrix

    return np.array(matrix)


def KNN(X_train, X_test, Y_train, K):

    pred = []

    def getNeighbors(xtrain, ytrain, xtest, K):
        euclid = [] # all neighbors
        length = int(len(xtrain)/len(xtest)) # getting length for repeated test
        tile = np.tile(xtest, (length, 1)) # repeat test to fit length of train
        e = getEuclidDistance(xtest, xtrain)    # compute distances
        euclid.append((xtrain, e, ytrain))      # append it
        euclid.sort(key=lambda j: j[1])
        neighbors = euclid[:K]      # only K neighbors

        return neighbors
    def getvote(neighbors):

        counter = Counter()
        for n in neighbors:
            counter[int(n[2][0])] += 1
        return counter.most_common(1)[0][0]

    for i in range(len(X_test)):
        neighbors = getNeighbors(X_train, Y_train, X_test[i], K)
        pred.append(getvote(neighbors))
    return np.asarray(pred)


################## Random Tree Setup ####################
# Gini formula from piazza @239
def gini(group, y_train, classes):
    length = len(group)
    d = y_train
    sum = 0
    for i in range(len(d)):
        probability = d[int(i-1)]/length
        sum+=probability**2
    return 1 - sum

# Gain formula from piazza @239
def gain(group, y_train, classes):
    s = sum([len(i) for i in group])
    rows = [r for g in group for r in g]
    ginis = gini(rows, y_train, classes)
    for g in group:
        ginis -= gini(group, y_train, classes) *len(group)/s
    return ginis

# left and right nodes of tree
def sep(i, v, X_train):
    left_of_node = []
    right_of_node = []
    for x in X_train:
        if x[i] < v:
            left_of_node.append(x)
        else:
            right_of_node.append(x)
        return [left_of_node, right_of_node]


# all possible splits
def splitter(X_train, y_train, i):

    classes = y_train
    spv, big_ig, spg = 0, -1, None
    for x in X_train:
        g = sep(i, x[i], X_train)
        ig = gain(g, y_train, classes)
        if ig > big_ig:
            spv, big_ig, spg = x[i], ig, g
        return {'i': i, 'spv': spv, 'g': g}

def tree(X_train, y_train, depth, size):

    randomness = int( np.random.random()*(len(X_train[0]) - 1))
    tree_root = splitter(X_train, y_train, randomness)
    tree_splitter(tree_root, depth, size, 1, y_train)

    return tree_root

def final(g, y_train):

    classes = list()

    for i in range(len(y_train)):
        classes.append(y_train[i][0])

    return max(set(classes), key=classes.count)

def tree_splitter(tree_node, depth, size, curr, y_train):
    left_node, right_node = tree_node['g']
    del(tree_node['g'])

    if not right_node or not left_node:
        tree_node['l'] = tree_node['r'] = final(left_node + right_node, y_train)
        return

    if curr >= depth:
        tree_node['l'] = final(left_node, y_train)
        tree_node['r'] = final(right_node, y_train)
        return

    if len(left_node) > size:
        i = int( np.random.random()*(len(right_node[0]) - 1))
        left_node['l'] = splitter(left_node, i)
        tree_splitter(left_node['l'], depth, size, curr+1)
    else:
        left_node['l'] = final(left_node, y_train)

    if len(right_node) > size:
        i = int( np.random.random()*(len(right_node[0]) - 1))
        right_node['r'] = splitter(right_node, i)
        tree_splitter(right_node['r'], depth, size, curr+1)
    else:
        right_node['r'] = final(right_node, y_train)

def making_forest(X_train, y_train, m , trees):
    depth = 500
    size = 200
    f = []
    for i in range(0, trees):
        index = np.random.choice(len(X_train), m)
        f.append(tree(X_train[index], y_train[index], depth, size))
    return f

def run_tree(node, row):
    if row[node['i']] < node['spv']:
        if isinstance(node['l'], dict):
            return run_tree(node['l'], row)
        else:
            return node['l']
    else:
        if isinstance(node['r'], dict):
            return run_tree(node['r'], row)
        else:
            return node['r']

def predict(forest, row):
    classes = []
    for tree_root in forest:
        classes.append(run_tree(tree_root, row))
    return max(set(classes), key=classes.count)

def RandomForest(X_train,Y_train,X_test):
    """
    :type X_train: numpy.ndarray
    :type X_test: numpy.ndarray
    :type Y_train: numpy.ndarray
    
    :rtype: numpy.ndarray
    """
    y_pred = list()
    forester = making_forest(X_train, Y_train, m=3000, trees=500)
    for row in X_train:
        prediction = predict(forester, row)
        y_pred.append(prediction)
    return np.asarray(y_pred)

##################### END RANDOMFOREST ######################################


def PCA(X_train, N):
    """
    :type X_train: numpy.ndarray
    :type N: int
    :rtype: numpy.ndarray
    """

    mean = np.mean(X_train.transpose(), axis=1)
    center = X_train - mean

    covariance = np.cov(center.transpose())

    eig_values, eig_vectors = np.linalg.eig(covariance)

    eig_values = eig_values[0:N]
    eig_vectors = eig_vectors[:, 0:N]

    sorted = np.flip(np.argsort(eig_values))
    eig_vectors = eig_vectors[:, sorted]

    ans = (np.dot(eig_vectors.transpose(), center.transpose())).transpose()
    return ans

    
def Kmeans(X_train, N):
    """
    :type X_train: numpy.ndarray
    :type N: int
    :rtype: List[numpy.ndarray]
    """

    centroids = {}
    classify = {}
    random_indexes = list()

    for m in range(N):
        classify[m] = []


    # Random N centroids
    for w in range(N):
        r_index = np.random.randint(0, X_train.shape[0])    # random centroid

        if r_index not in random_indexes:   # if index not in random index list, append it
            random_indexes.append(r_index)
        else:
            while r_index in random_indexes:    # randomize index again if in list
                r_index = np.random.randint(0, X_train.shape[0])
            random_indexes.append(r_index)

    # Get centroids and add them to list
    for i in range(N):
        index = random_indexes[i]
        centroids[i] = (X_train[index])

    # compute distances, compute closest distance, then append closest
    for x in X_train:
        euclid_distances = [getEuclidDistance(x, centroids[y]) for y in centroids]
        classify[euclid_distances.index(min(euclid_distances))].append(x)

    # get average
    for k in classify:
        centroids[k] = np.average(classify[k], axis=0)

    convert = list()
    #convert dictionary to nparray
    for f in range(len(centroids)):
        convert.append(np.asarray(centroids.get(f)))

    centroids = convert

    return centroids






################################################ PART 2 ##########################################################

from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV



def SklearnSupervisedLearning(X_train,Y_train,X_test, Y_test):

    """
    :type X_train: numpy.ndarray
    :type X_test: numpy.ndarray
    :type Y_train: numpy.ndarray
    
    :rtype: List[numpy.ndarray] 
    """
    # SVM
    svm_classifier = svm.SVC(kernel='linear', C = 1)
    svm_classifier.fit(X_train, Y_train.ravel())

    svm_ypred = svm_classifier.predict(X_test)

    print('SVM Accuracy: ', accuracy_score(Y_test, svm_ypred))

    # Logistic Regression
    logreg_classifier = LogisticRegression(max_iter=700)
    logreg_classifier.fit(X_train, Y_train.ravel())

    logreg_ypred = logreg_classifier.predict(X_test)
    print('Regression Accuracy: ', accuracy_score(Y_test, logreg_ypred))

    # Decision Tree
    dtree_classifer = DecisionTreeClassifier()
    dtree_classifer.fit(X_train, Y_train.ravel())

    dtree_ypred = dtree_classifer.predict(X_test)
    print('Decision Tree Accuracy:', accuracy_score(Y_test, dtree_ypred))

    # KNN
    knn_classifier = KNeighborsClassifier(8)
    knn_classifier.fit(X_train, Y_train.ravel())

    knn_ypred = knn_classifier.predict(X_test)
    print('KNN Accuracy: ', accuracy_score(Y_test, knn_ypred))

    plotConfusion(svm_classifier, logreg_classifier, dtree_classifer, knn_classifier, X_test, y_test)

    return svm_ypred, logreg_ypred, dtree_ypred, knn_ypred



def SklearnVotingClassifier(X_train,Y_train,X_test, Y_test):

    
    """
    :type X_train: numpy.ndarray
    :type X_test: numpy.ndarray
    :type Y_train: numpy.ndarray
    
    :rtype: List[numpy.ndarray] 
    """
    # SVM
    svm_classifier = svm.SVC(kernel='linear', C=1)
    svm_classifier.fit(X_train, Y_train.ravel())

    # Logistic Regression
    logreg_classifier = LogisticRegression(max_iter=700)
    logreg_classifier.fit(X_train, Y_train.ravel())

    # Decision Tree
    dtree_classifer = DecisionTreeClassifier()
    dtree_classifer.fit(X_train, Y_train.ravel())

    # KNN
    knn_classifier = KNeighborsClassifier(8)
    knn_classifier.fit(X_train, Y_train.ravel())

    voting_clf = VotingClassifier(estimators=[('SVM', svm_classifier), ('DTree', dtree_classifer),
                                              ('LogReg', logreg_classifier), ('KNN', knn_classifier)], voting='hard')

    voting_clf.fit(X_train, Y_train.ravel())
    voting_ypred = voting_clf.predict(X_test)

    print('Voting Classifier Accuracy: ', accuracy_score(Y_test, voting_ypred))

    return voting_ypred


"""
Create your own custom functions for Matplotlib visualization of hyperparameter search. 
Make sure that plots are labeled and proper legends are used
"""

from sklearn.metrics import plot_confusion_matrix

# Plots confusion matrix
def plotConfusion(supportvm, logreg, decision, knn, X_test, y_test):

    # Support Vector Machine
    s = plot_confusion_matrix(supportvm, X_test, y_test, cmap=plt.cm.Blues)
    s.ax_.set_title('Support Vector Machine')
    plt.show()

    # Logistic Regression
    lr = plot_confusion_matrix(logreg, X_test, y_test, cmap=plt.cm.Blues)
    lr.ax_.set_title('Logistic Regression')
    plt.show()

    # Decision Tree
    dt = plot_confusion_matrix(decision, X_test, y_test, cmap=plt.cm.Blues)
    dt.ax_.set_title('Decision Tree')
    plt.show()

    # K-Nearest Neighbor
    kn = plot_confusion_matrix(knn, X_test, y_test, cmap=plt.cm.Blues)
    kn.ax_.set_title('K-Nearest Neighbor')
    plt.show()



# Also plots parameters vs scores
def gridSearching(X_train, y_train, X_test, y_test):


    # Support Vector
    svm_grid = {'C': [0.1, 1, 10, 15, 20],
                  'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
                  'kernel': ['linear']}

    svmgrid = GridSearchCV(svm.SVC(), svm_grid, refit=True, verbose=3)
    svmgrid.fit(X_train, y_train.ravel())
    svm_pred = svmgrid.predict(X_test)
    print('Best Estimator for SVM:', svmgrid.best_estimator_)

    plt.title('Gamma vs Mean Score')
    plt.plot(svm_grid.get('gamma'), svmgrid.cv_results_.get('mean_test_score'))
    plt.legend()
    plt.xlabel('Gamma')
    plt.ylabel('Mean score')
    plt.show()



    # Decision Tree
    decision = {'criterion': ['gini', 'entropy'],
                'max_depth': [4, 8, 16, 20]}

    decisiongrid = GridSearchCV(DecisionTreeClassifier(), decision, refit=True, verbose=3)
    decisiongrid.fit(X_test, y_train.ravel())
    decision_pred = decisiongrid.predict(X_test)
    print('Best Estimator for Decision Tree:', decisiongrid.best_estimator_)

    plt.title('Max Depth vs Mean Score')
    plt.plot(decision.get('max_depth'), decisiongrid.cv_results_.get('mean_test_score'))
    plt.legend()
    plt.xlabel('Max Depth')
    plt.ylabel('Mean score')
    plt.show()


    # KNN
    knn = {'n_neighbors': [5, 6, 7, 8, 9, 10]}
    knngrid = GridSearchCV(KNeighborsClassifier(), knn, refit=True, verbose=3)
    knngrid.fit(X_test, y_train.ravel())
    knn_pred = knngrid.predict(X_test)
    print('Best Estimator for KNN:', knngrid.best_estimator_)

    plt.title('Number of Neighbors vs Mean Score')
    plt.plot(knn.get('n_neighbors'), knngrid.cv_results_.get('mean_test_score'))
    plt.legend()
    plt.xlabel('Number of Neighbors')
    plt.ylabel('Mean score')
    plt.show()


# Change CSV name here
X_train, y_train, X_test, y_test = getData('data.csv')




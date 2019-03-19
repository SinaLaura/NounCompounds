import json
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score

def add_classes(vector_dict):
    
    with open('Data/tratz2011_coarse_grained_lexical_full/train.tsv') as compFile:
        lines = compFile.readlines()
    
    tratz_compounds = {}
    relation_classes = {}
    for line in lines:
        splt = line.split('\t')
        compound = splt[0] + ' ' + splt[1]
        relation_class = splt[2]
        if not relation_class in relation_classes:
            relation_classes[relation_class] = len(relation_classes.keys())
        tratz_compounds[compound] = splt[2]

    feat_vectors = []
    targets = []
    for key, value in vector_dict.items():
        if key in tratz_compounds:
            feat_vector = list(value.values())
            if has_non_zeroes(feat_vector):
                feat_vectors.append(feat_vector)
                targets.append(relation_classes[tratz_compounds[key]])
    return feat_vectors, targets

def has_non_zeroes(lst):
    ret = False
    for item in lst:
        if item > 0:
            ret = True
    return ret

def classify(features, targets):
    
    clf = svm.SVC(gamma='scale')
    result = cross_val_score(clf, features, targets, scoring = 'accuracy', cv = 2)
    print(result)
    
def get_pseudo_data():
    features = np.random.randint(0, 10, [4000, 200])
    targets = np.random.randint(0, 12, [4000])

    return features, targets

with open("sem_rel_compounds_vec.json") as test:
    dictionary = json.load(test)

print('Testing Constantins Data:')
features, targets = add_classes(dictionary)
'''
split_point = len(features) / 10 * 9
train_features = features[:split_point]
test_features = features[split_point:]
train_targets = targets[:split_point]
test_targets = targets[split_point:]
'''
classify(features, targets)

print('Testing randomly generated Data as baseline estimate:')
features, targets = get_pseudo_data()
classify(features, targets)


import competition_utilities as cu
import features
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from threading import Thread
from sklearn import  svm


train_file = "train-sample_October_9_2012_v2.csv"
feature_file1="feature_set.csv"
feature_file2="feature_set1.csv"
full_train_file = "train.csv"
test_file = "test1.csv"
submission_file = "basic_benchmark.csv"


def main():
    print("Reading the data")
    data = cu.get_dataframe(train_file)

    #print("Extracting features")
    #features.compute_features(train_file,feature_file1)

    print("Training the model")
    fea = cu.get_dataframe(feature_file1)
    clf = svm.SVC(decision_function_shape='ovo')
    clf.fit(fea, data["OpenStatus"][:178351])

    print("Reading test file and making predictions")
    #features.compute_features("test_.csv",feature_file2)
    test_fea = cu.get_dataframe(feature_file2)
    probs = clf.predict_proba(test_fea)

    print("Calculating priors and updating posteriors")
    new_priors = cu.get_priors(full_train_file)
    old_priors = cu.get_priors(train_file)
    probs = cu.cap_and_update_priors(old_priors, probs, new_priors, 0.001)

    print("Saving submission to %s" % submission_file)

    cu.write_submission(submission_file, probs)

if __name__=="__main__":
    main()




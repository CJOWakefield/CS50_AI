import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    months = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
              'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}

    visitors = {'Returning_Visitor': 1, 'New_Visitor': 0, 'Other': 0}

    evidence = []
    labels = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            row_data = []
            # Administrative,Administrative_Duration,Informational,Informational_Duration,
            # ProductRelated,ProductRelated_Duration,
            # BounceRates,ExitRates,PageValues,SpecialDay,
            # Month,OperatingSystems,Browser,Region,TrafficType,VisitorType,Weekend,Revenue
            row_data.append(int(row['Administrative']))
            row_data.append(float(row['Administrative_Duration']))
            row_data.append(int(row['Informational']))
            row_data.append(float(row['Informational_Duration']))
            row_data.append(int(row['ProductRelated']))
            row_data.append(float(row['ProductRelated_Duration']))
            row_data.append(float(row['BounceRates']))
            row_data.append(float(row['ExitRates']))
            row_data.append(float(row['PageValues']))
            row_data.append(float(row['SpecialDay']))
            row_data.append(months[row['Month']])
            row_data.append(int(row['OperatingSystems']))
            row_data.append(int(row['Browser']))
            row_data.append(int(row['Region']))
            row_data.append(int(row['TrafficType']))
            row_data.append(visitors[row['VisitorType']])
            row_data.append(1 if row['Weekend'] else 0)

            # Data and labels added
            evidence.append(row_data)
            labels.append(1 if row['Revenue'] else 0)

        return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    buy = labels.count(1)
    no_buy = labels.count(0)

    correct_positive, correct_negative = 0, 0

    for i in range(len(predictions)):
        # prediction matches true label
        if predictions[i] == labels[i]:
            if predictions[i] == 1:
                correct_positive += 1
            else:
                correct_negative += 1

    # Proportion of correct purchase predictions
    if buy:
        sensitivity = (correct_positive / buy)
    else:
        sensitivity = 0
    # Proportion of correct no-purchase predictions
    if no_buy:
        specificity = (correct_negative / no_buy)
    else:
        specificity = 0

    return sensitivity, specificity


if __name__ == "__main__":
    main()

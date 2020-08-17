import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

floats = ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']
ints = ['Administrative', 'Informational', 'ProductRelated', 'Month', 'OperatingSystems', 'Browser', 'Region', 'TrafficType', 'VisitorType', 'Weekend']
MONTHS = ['Jan','Feb','Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    y_train, y_test, X_train, X_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(y_train, X_train)
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
    
    evidence = []
    labels = []
    
    # Opening file and iterating through rows
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)

        first_row = True
        col_names = []

        for row in csv_reader:
            # In the first row, the labbels are copied
            if first_row:
                col_names = row.copy()
                first_row = False
        
            else:
                # Other rows: Check every value in a row
                new_list = []
                for index in range(len(col_names)):
                    str_value = row[index]
                    col_name = col_names[index]

                    # If the column is the revenue, we have the evidence
                    if col_name == 'Revenue':
                        evidence.append(int(str_value == 'TRUE'))
                    # Otherwise, we use an auxiliar function, get_value
                    else:
                        new_list.append(get_value(str_value, col_name))

                labels.append(new_list)

        return evidence, labels


def get_value(str_value, label):
    """
    Gets the numeric value depending on the label of the column
    """
    if label == 'Month':
        return MONTHS.index(str_value)

    elif label == 'VisitorType':
        return int(str_value == 'Returning_Visitor')
    
    elif label == 'Weekend':
        return int(str_value == 'TRUE') 
    
    elif label in floats:
        return float(str_value)
    
    else:
        return int(str_value)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors = 1)
    model.fit(labels, evidence)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    size_1 = 0
    size_0 = 0
    specificity = 0
    length = len(predictions)
    # For each prediction, the hits are tracked. The size of each result is calculated
    for index in range(length):
        if predictions[index] == 1:
            sensitivity += int(labels[index] == predictions[index])
            size_1 += 1
        else:
            specificity += int(labels[index] == predictions[index])
            size_0 += 1
            
    return sensitivity / size_1, specificity / size_0


if __name__ == "__main__":
    main()

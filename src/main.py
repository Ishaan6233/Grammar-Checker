import csv
import os

import nltk
from nltk import CFG


# Load the grammar from a CFG file located at 'grammars/' folder
def load_cfg_grammar(grammar_file_path):
    try:
        with open(grammar_file_path, 'r') as grammar_file:
            # Loading the context-free grammar from file
            toy_grammar = CFG.fromstring(grammar_file.read())
        return toy_grammar
    except FileNotFoundError:
        print(f"Error: The grammar file at {grammar_file_path} was not found.")
        return


# Load the dataset (POS tagged sentences) from a TSV file in the 'data/' folder
def load_data(tsv_file_path):
    data = []
    try:
        with open(tsv_file_path, newline='') as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter='\t')
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: The data file at {tsv_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
    return data


# Parse the POS sequences and store the results
def parse(output_file_path, data, parser):
    try:
        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file, delimiter='\t')
            writer.writerow(['id', 'ground_truth', 'prediction'])  # Headers

            for row in data:
                sentence_id = row['id']
                ground_truth = row['label']  # The correct grammar classification from the dataset
                pos_sequence = row['pos']  # The POS-tag sequence (e.g., DT NN VBZ)

                # Split POS sequence and handle special characters
                pos_tags = pos_sequence.split()  # Tokenize the POS sequence
                prediction = 1  # Default to "error detected"

                try:
                    # Try to parse the sequence using NLTK ChartParser
                    list(parser.parse(pos_tags))  # Need to iterate to trigger parsing
                    prediction = 0  # If parsing succeeds, no grammar errors
                except (ValueError, StopIteration):
                    prediction = 1  # If parsing fails, grammar error detected

                # Debugging print to check each pair of ground truth and prediction
                # print(f"Sentence ID: {sentence_id}, Ground Truth: {ground_truth}, Prediction: {prediction}")

                writer.writerow([sentence_id, ground_truth, prediction])  # Write results

    except Exception as e:
        print(f"Error writing to output file: {e}")


# Confusion matrix calculation
def calculate_confusion_matrix(results):
    TP = FP = FN = TN = 0

    for row in results:
        ground_truth = int(row['ground_truth'])
        prediction = int(row['prediction'])

        if ground_truth == 1 and prediction == 1:
            TP += 1  # True Positive --> both predicted and actual label indicate error
        elif ground_truth == 0 and prediction == 1:
            FP += 1  # False Positive --> predicted error, but the actual label is correct
        elif ground_truth == 1 and prediction == 0:
            FN += 1  # False Negative --> predicted correct, but the actual label indicates an error
        elif ground_truth == 0 and prediction == 0:
            TN += 1  # True Negative -->  both predicted and actual label indicate no error

    return TP, FP, FN, TN


# Calculate precision and recall from confusion matrix values
def calculate_precision_recall(TP, FP, FN):
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    return precision, recall


# Evaluate grammar predictions: load results, calculate precision and recall
def evaluate_grammar(results_file):
    results = []
    try:
        with open(results_file, newline='') as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter='\t')
            for row in reader:
                results.append(row)

        TP, FP, FN, TN = calculate_confusion_matrix(results)

        # Compute and display precision and recall
        precision, recall = calculate_precision_recall(TP, FP, FN)
        print(f'Precision: {precision:.4f}')
        print(f'Recall: {recall:.4f}')

    except FileNotFoundError:
        print(f"Error: The results file at {results_file} was not found.")
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")

    return precision, recall


def main(input_tsv_file, grammar_file, output_tsv_file):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_tsv_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the output directory if it doesn't exist

    grammar = load_cfg_grammar(grammar_file)  # Grammar is loaded
    if grammar is None:
        print("Cannot proceed without a valid grammar file.")
        return

    parser = nltk.ChartParser(grammar)  # Initialize parser
    data = load_data(input_tsv_file)  # Load dataset

    if len(data) == 0:
        print("No data available for parsing.")
        return

    # Parse the dataset and write the results to output
    parse(output_tsv_file, data, parser)

    # Evaluate the performance
    evaluate_grammar(output_tsv_file)


if __name__ == '__main__':
    root = './'  # Set root to current working directory

    input_tsv_file = root + 'data/train.tsv'  # Dataset of POS-tagged sentences
    grammar_file = root + 'grammars/toy.cfg'  # Grammar rules
    output_tsv_file = root + 'output/train_results.tsv'  # Results of parsing

    main(input_tsv_file, grammar_file, output_tsv_file)

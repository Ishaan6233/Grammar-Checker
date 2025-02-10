``` This project is a basic grammar checker built using ***Context-Free Grammar (CFG) and constituency parsing**. The grammar checker analyzes the **part-of-speech (POS) tag sequences of sentences** to determine whether they are grammatically **correct or incorrect**. It compares the POS sequence to a set of CFG (toy) rules, and based on whether the sentence can be parsed successfully, the sentence is classified as either **grammatically correct (error-free)** or **incorrect (contains grammar errors)**. ```

## Requirements ##
To run this project, make sure the following are installed:
- **Python 3.x**: The code is written for Python 3.x versions.
- **NLTK (Natural Language Toolkit)**: Required for grammar parsing using CFG.
- **CSV Library**: This is part of Python's standard library and doesn't require installation.

### Installing Required Libraries
Use the following commands to ensure the required libraries are available to use:

1. **Installing NLTK**:
``` python3 -m pip install --user nltk```

2. Downloading NLTK Resources: NLTK requires some additional data for grammar parsing. To ensure proper functionality, add the following snippet to your code or run it separately to download the required resources:

  ```
  import nltk
  nltk.download('punkt')
  ```

## File Structure ##

```
├── grammars/
│   └── toy.cfg       # Toy grammar in CFG format
├── data/
│   └── train.tsv     # Input dataset containing POS-tagged sentences
├── output/
│   └── train_results.tsv # Output file with grammar check results
├── src/
│   └── main.py       # Main Python file containing the grammar checker implementation
└── README.md         # This README file
```

## Usage ##

The program expects three positional arguments when executed:
- Path to the input data file (train.tsv).
- Path to the grammar file (toy.cfg).
- Path to the output file where results will be stored.
Command:  python3 src/main.py data/train.tsv grammars/toy.cfg output/train_results.tsv

### Input File (train.tsv) ###
The input file contains tab-separated values with the following structure:
- id: Unique identifier for each sentence.
- label: Indicates whether the sentence contains a grammar error (1) or is error-free (0).
- sentence: The original sentence in tokenized form.
- pos: POS tags corresponding to each word in the sentence.

### Output File (train_results.tsv) ###
The output file will contain three columns:
- id: The sentence ID from the input file.
- ground_truth: The correct label (from the input file) indicating whether the sentence contains grammar errors.
- prediction: The result from the grammar checker (1 for errors, 0 for error-free).

## Execution
Example usage: use the following command in the current directory.

`python3 src/main.py data/train.tsv grammars/toy.cfg output/train.tsv`

## How It Works ##
- Loading Grammar: The toy CFG is loaded from the toy.cfg file, defining English grammar rules in CFG format.
- Parsing Sentences: The input POS-tagged sentences are parsed using NLTK's ChartParser. If the sentence can be parsed successfully according to the grammar, it is marked as grammatically correct (prediction = 0). Otherwise, it is marked as containing errors (prediction = 1).
- Evaluation: After parsing, precision and recall are calculated based on the predicted and ground truth labels.

## Precision and Recall ##
- Precision: Measures how many of the sentences predicted to contain grammar errors are actually incorrect.
- Recall: Measures how many of the actual incorrect sentences were identified by the checker.

## Error Analysis ##
- To perform error analysis, look at the output file and manually compare the predictions with the ground truth. Identify cases where the grammar checker failed

## Report ##
- Precision, recall, and error analysis are documented in the report file included with the submission. The report also answers questions about the limitations and potential improvements for the grammar checker.
  
## References and Acknowledgments
Below are some of the external resources (websites) I consulted to better understand different components for the requirements of the assignment:

- **NLTK Documentation**: I relied on the NLTK documentation to learn more about how the `ChartParser` and `CFG` work, and to better understand how to debug parsing in Python.  
  [https://www.nltk.org](https://www.nltk.org)

- **Stack Overflow**: Stack Overflow was incredibly helpful for troubleshooting installation issues and understanding how to work with various NLTK components and CFG parsing methods.  
  [https://stackoverflow.com](https://stackoverflow.com)

- **YouTube Video**: This video helped me better understand the inner workings of constituency parsing with CFG and NLTK.
  [Youtube Video - Context Free Grammar](https://www.youtube.com/watch?v=kq4aUYzLlb0)



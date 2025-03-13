# Eye-tracking Data Analysis Pipeline

This folder contains scripts for analyzing eye-tracking data from the Zuco dataset, focusing on word skipping and regression patterns during reading.

## Processing Pipeline

1. **Extract Eye-tracking Data**
```bash
python process_extracted_results.py
```
- Processes raw eye-tracking data
- Calculates fixation sequences and reading patterns
- Outputs processed data to `zuco/bai_extracted_task2_NR_ET/`

2. **Create Word Frequencies**
```bash
python create_word_frequencies.py
```
- Downloads and processes SUBTLEX word frequencies
- Calculates frequency per million and log frequencies
- Outputs to `word_frequencies.json`

3. **Create Raw Sentences Dataset**
```bash
python create_raw_sentences.py
```
- Extracts sentences from relations_labels_task2.csv
- Creates word indices for each sentence
- Outputs to `raw_sentences.json`

4. **Calculate Word Predictabilities**
```bash
python create_word_predictabilities.py
```
- Calculates word predictabilities using NLTK language model
- Computes both raw and logit-transformed predictabilities
- Uses full sentence context for each word
- Outputs to `word_predictabilities.json`

5. **Create Comprehensive Sentences Dataset**
```bash
python create_sentences_dataset.py
```
- Combines data from multiple sources:
  - Raw sentences from `raw_sentences.json`
  - Word frequencies from `word_frequencies.json`
  - Word predictabilities from `word_predictabilities.json`
- Creates comprehensive word-level features:
  - Word ID and content
  - Length, frequency, and difficulty
  - Predictability and logit values
- Outputs to `sentences_dataset.json`

6. **Analyze Reading Patterns**
```bash
python analyze_reading_patterns.py
```
- Analyzes word-level reading behaviors
- Calculates skipping and regression patterns
- Uses word frequencies to compute difficulty metrics
- Outputs to `zuco/bai_reading_pattern_analysis/`

7. **Analyze Word Probabilities**
```bash
python analyze_word_probabilities.py
```
- Calculates word skipping and regression probabilities at the individual word occurrence level
- Each word occurrence is uniquely identified by:
  - Sentence ID
  - Word position in sentence
  - Word itself
- Analyzes effects of word length, frequency, and difficulty
- Creates visualization plots and statistical summaries
- Outputs to `zuco/bai_word_probability_analysis/`

## Output Structure

```
scripts/data/
├── raw_sentences.json                  # Raw sentences with word indices
├── word_frequencies.json              # Word frequency data
├── word_predictabilities.json         # Word predictability scores
├── sentences_dataset.json             # Comprehensive word-level features
├── zuco/
│   ├── bai_extracted_task2_NR_ET/     # Processed eye-tracking data
│   │   └── *_NR_processed.json
│   ├── bai_reading_pattern_analysis/  # Word-level reading patterns
│   │   └── *_reading_patterns.json
│   └── bai_word_probability_analysis/ # Statistical analysis
│       ├── plots/                     # Visualization plots
│       │   ├── length_skip_effect.png
│       │   ├── frequency_skip_effect.png
│       │   ├── difficulty_regression_effect.png
│       │   └── predictability_skip_effect.png
│       ├── word_skipping_analysis.csv # Detailed skipping statistics
│       ├── word_regression_analysis.csv # Detailed regression statistics
│       ├── complete_word_analysis.csv # Full word-level analysis
│       └── analysis_summary.txt       # Statistical summary
```

## Analysis Details

### Word Features Analyzed
- Word length
- Word frequency (from SUBTLEX)
- Word difficulty (based on SWIFT model)
- Word predictability (based on NLTK language model)
- Logit-transformed predictability

### Reading Behaviors
- First-pass word skipping (calculated per unique word occurrence)
- Word regression patterns (calculated per unique word occurrence)
- Eye-tracking metrics (FFD, GD, TRT, etc.)

### Statistical Measures
- Skip and regression probabilities (calculated per unique word occurrence)
- Correlations with word features
- Distribution statistics
- Confidence intervals

## Requirements

Required Python packages:
```bash
pip install numpy pandas matplotlib seaborn nltk tqdm
```

## Notes

- Word frequencies are based on SUBTLEX corpus
- Word difficulty is calculated using the SWIFT model
- Word predictabilities are calculated using NLTK language model with full sentence context
- All analyses exclude punctuation marks and use lowercase words
- Regression analysis only considers short-distance regressions (≤ 5 words)
- Word probabilities are calculated at the individual occurrence level, capturing how the same word can have different reading patterns depending on its context and position in the sentence 
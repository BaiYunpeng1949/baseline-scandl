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

3. **Analyze Reading Patterns**
```bash
python analyze_reading_patterns.py
```
- Analyzes word-level reading behaviors
- Calculates skipping and regression patterns
- Uses word frequencies to compute difficulty metrics
- Outputs to `zuco/bai_reading_pattern_analysis/`

4. **Analyze Word Probabilities**
```bash
python analyze_word_probabilities.py
```
- Calculates word skipping and regression probabilities
- Analyzes effects of word length, frequency, and difficulty
- Creates visualization plots and statistical summaries
- Outputs to `zuco/bai_word_probability_analysis/`

## Output Structure

```
zuco/
├── bai_extracted_task2_NR_ET/          # Processed eye-tracking data
│   └── *_NR_processed.json
├── bai_reading_pattern_analysis/        # Word-level reading patterns
│   └── *_reading_patterns.json
└── bai_word_probability_analysis/       # Statistical analysis
    ├── plots/                          # Visualization plots
    │   ├── length_skip_effect.png
    │   ├── frequency_skip_effect.png
    │   ├── difficulty_regression_effect.png
    │   └── predictability_skip_effect.png
    ├── word_skipping_analysis.csv      # Detailed skipping statistics
    ├── word_regression_analysis.csv     # Detailed regression statistics
    ├── complete_word_analysis.csv       # Full word-level analysis
    └── analysis_summary.txt            # Statistical summary

## Analysis Details

### Word Features Analyzed
- Word length
- Word frequency (from SUBTLEX)
- Word difficulty (based on SWIFT model)
- Word predictability (placeholder for future LLM implementation)

### Reading Behaviors
- First-pass word skipping
- Word regression patterns
- Eye-tracking metrics (FFD, GD, TRT, etc.)

### Statistical Measures
- Skip and regression probabilities
- Correlations with word features
- Distribution statistics
- Confidence intervals

## Requirements

Required Python packages:
```bash
pip install numpy pandas matplotlib seaborn
```

## Notes

- Word frequencies are based on SUBTLEX corpus
- Word difficulty is calculated using the SWIFT model
- Predictability values are currently placeholders (set to 0)
- All analyses exclude punctuation marks and use lowercase words
- Regression analysis only considers short-distance regressions (≤ 5 words) 
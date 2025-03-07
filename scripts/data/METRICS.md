# Eye-tracking Metrics Documentation

This document describes all metrics calculated in our eye-tracking analysis pipeline.

## Basic Information Metrics

- `sentence_length`: Number of words in the sentence
- `sentence_id`: Unique identifier for each sentence
- `sentence_content`: The actual text content of the sentence

## Word-Level Eye-tracking Metrics

These metrics are calculated for each word and then averaged across the sentence:

- `FFD` (First Fixation Duration): Duration of the first fixation on a word
- `GD` (Gaze Duration): Sum of all fixations on a word during first-pass reading
- `GPT` (Go-Past Time): Sum of all fixations from first entering a word until moving past it to the right
- `TRT` (Total Reading Time): Sum of all fixations on a word
- `nFixations`: Number of fixations on a word
- `meanPupilSize`: Average pupil size during word fixations

## Word Skipping Metrics

- `skipped_words`: Set of word indices that were skipped during reading
- `skip_pairs`: List of (from, to) pairs indicating skipping events
- `skipped_words_count`: Total number of words skipped, calculated as the sum of skip distances
  - For each skip pair (m,n), adds (n-m-1) to the count
  - Example: Skip pair (1,4) means words 2 and 3 were skipped, adding 2 to the count
- `word_skip_rate`: `skipped_words_count` divided by total sentence length
- `max_skip_distance`: Maximum number of words skipped in a single skip event

A word skip is counted when:
1. Moving forward (current_word > prev_word)
2. Gap exists between words (current_word - prev_word > 1)
3. Either:
   - Both words are in first pass (not seen before), or
   - Landing word is in first pass

## Regression Metrics

- `regressed_words`: Set of word indices that were regressed to
- `regression_pairs`: List of (from, to) pairs indicating regression events
- `regressed_words_count`: Total number of regression events (count of regression pairs)
- `word_regression_rate`: `regressed_words_count` divided by total sentence length
- `max_regression_distance`: Maximum number of words moved backward in a single regression

A regression is counted when:
1. Moving backward (current_word < prev_word)
2. Regression distance ≤ 5 words (short-distance regressions only)

## Combined Metrics

- `skipped_then_regressed_proportion`: Proportion of regressed words that were initially skipped
  - Calculated as: |skipped_words ∩ regressed_words| / |regressed_words|
  - Example: If regressed_words={0,2,3,5,8,10,11,12,13,15,17,18,20} and 
    skipped_words={1,4,5,7,8,9,10,11,12,13,14,20,21}, then
    proportion = |{5,8,10,11,12,13,20}| / |regressed_words| = 7/13

## Fixation-based Metrics

Original metrics from raw fixation data:

- `fixation_omission_rate`: Proportion of words with no fixations
- `fixation_regression_rate`: Proportion of backward eye movements in fixation sequence

## Output Files

Metrics are saved in three types of files:

1. Individual participant files (`{participant_id}_sentence_metrics.csv`):
   - Contains all metrics for each sentence read by the participant

2. Participant-wise metrics (`12_participants_wise_metrics.csv`):
   - Contains mean and standard deviation of each metric per participant

3. Overall metrics (`overall_metrics.csv`):
   - Contains global mean and standard deviation of each metric across all sentences
   - Includes metadata like total sentences and participants

## Reading Sequence Processing

- `word_sequence`: Normalized sequence of word indices in reading order
- First pass reading: When a word is fixated for the first time
- Words are considered "seen" after their first fixation
- Reading sequence is normalized to start from the first occurrence of the smallest word index 
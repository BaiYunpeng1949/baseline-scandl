import os
import json
import pandas as pd
import numpy as np
from glob import glob

def safe_mean(values):
    """Safely calculate mean of a list of values, handling None and non-list values"""
    if not values:
        return None
    # Convert single values to list
    if not isinstance(values, list):
        values = [values]
    # Filter out None values and convert to float
    valid_values = []
    for v in values:
        if v is not None:
            try:
                valid_values.append(float(v))
            except (ValueError, TypeError):
                continue
    if not valid_values:
        return None
    return np.mean(valid_values)

def normalize_reading_sequence(word_sequence):
    """Normalize reading sequence to start from the first occurrence of smallest word index"""
    if not word_sequence:
        return []
    
    # Find the smallest word index
    min_idx = min(word_sequence)
    # Find its first occurrence
    start_pos = word_sequence.index(min_idx)
    # Return sequence from that position
    return word_sequence[start_pos:]

def calculate_distances(sentence):
    """Calculate word skips and regressions based on reading sequence"""
    distances = {
        'word_sequence': [],          # Sequence of word indices in reading order
        'skipped_words': set(),       # Words skipped during forward reading
        'regressed_words': set(),     # Words that were regressed to
        'skip_pairs': [],            # List of (from, to) pairs for skips
        'regression_pairs': [],      # List of (from, to) pairs for regressions
        'max_skip_distance': 0,       # Maximum skip distance
        'max_regression_distance': 0   # Maximum regression distance
    }
    
    if 'fixation_sequence' not in sentence:
        return distances
    
    # Create a list of word indices in fixation order
    raw_word_sequence = []
    for fix in sentence['fixation_sequence']:
        raw_word_sequence.append(fix['word_idx'])
    
    # Normalize the sequence to start from the first occurrence of smallest word index
    word_sequence = normalize_reading_sequence(raw_word_sequence)
    distances['word_sequence'] = word_sequence
    
    if not word_sequence:
        return distances
    
    # Initialize tracking variables
    current_forward_pos = word_sequence[0]  # Position for tracking forward reading
    last_word = word_sequence[0]           # Last word read
    seen_words = {word_sequence[0]}        # Set of all words seen
    
    # Process the sequence
    for i in range(1, len(word_sequence)):
        current_word = word_sequence[i]
        
        if current_word > last_word:
            # Forward reading
            if current_word - current_forward_pos > 1:
                # Words were skipped
                distances['skip_pairs'].append((current_forward_pos, current_word))
                skip_distance = current_word - current_forward_pos - 1
                distances['max_skip_distance'] = max(distances['max_skip_distance'], skip_distance)
                # Add skipped words
                for skipped_idx in range(current_forward_pos + 1, current_word):
                    distances['skipped_words'].add(skipped_idx)
            current_forward_pos = current_word
        elif current_word < last_word:
            # Reading a previous word - this is a regression
            regression_distance = last_word - current_word
            # Only record regression if it's not a long-distance jump (threshold of 5 words)
            if regression_distance <= 5:
                distances['regression_pairs'].append((last_word, current_word))
                distances['regressed_words'].add(current_word)
                distances['max_regression_distance'] = max(distances['max_regression_distance'], regression_distance)
            # Reset forward reading position to handle subsequent forward reading correctly
            current_forward_pos = current_word
        
        last_word = current_word
        seen_words.add(current_word)
    
    return distances

def extract_word_metrics(sentence):
    """Extract word-level metrics from a sentence"""
    metrics = {
        'FFD': [], 'GD': [], 'GPT': [], 'TRT': [], 
        'nFixations': [], 'meanPupilSize': []
    }
    
    for word in sentence['words']:
        for metric in metrics.keys():
            value = word['metrics'].get(metric)
            if value is not None:
                try:
                    # Handle both single values and lists
                    if isinstance(value, (list, np.ndarray)):
                        value = value[0] if len(value) > 0 else None
                    metrics[metric].append(float(value))
                except (ValueError, TypeError):
                    metrics[metric].append(None)
            else:
                metrics[metric].append(None)
    
    return metrics

def extract_fixation_sequence(sentence):
    """Extract fixation sequence from a sentence"""
    fixations = []
    
    # Get all fixations from the sentence
    if 'fixation_sequence' in sentence:
        for fix in sentence['fixation_sequence']:
            fixations.append([fix['x'], fix['y'], fix['duration']])
    
    return fixations

def save_fixation_data(participant_id, sentence_id, fixations, output_dir):
    """Save fixation data to a JSON file"""
    # Create participant directory if it doesn't exist
    participant_dir = os.path.join(output_dir, participant_id)
    os.makedirs(participant_dir, exist_ok=True)
    
    # Create the fixation data structure
    fixation_data = {
        "fixations": fixations
    }
    
    # Save to JSON file
    output_file = os.path.join(participant_dir, f"sentence_{sentence_id}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixation_data, f)

def process_participant_json(json_file, metrics_output_dir, fixations_output_dir):
    """Process a single participant's JSON file and return a DataFrame with sentence-level metrics"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract participant ID from filename
        participant_id = os.path.basename(json_file).replace('_NR_processed.json', '')
        
        # Create a list to store sentence-level metrics
        sentence_metrics = []
        
        for sentence in data:
            try:
                # Extract word-level metrics
                word_metrics = extract_word_metrics(sentence)
                
                # Calculate distances and sequences
                distances = calculate_distances(sentence)
                
                # Calculate sentence-level metrics
                metrics = {
                    # Basic information
                    'participant_id': participant_id,
                    'sentence_id': sentence['sentence_id'],
                    'sentence_content': sentence['sentence_content'],
                    'sentence_length': len(sentence['words']),
                    
                    # Word sequences and sets
                    'word_sequence': ','.join(map(str, distances['word_sequence'])),
                    'skipped_words': ','.join(map(str, sorted(distances['skipped_words']))),
                    'regressed_words': ','.join(map(str, sorted(distances['regressed_words']))),
                    
                    # Skip and regression pairs
                    'skip_pairs': '; '.join([f"({a},{b})" for a, b in distances['skip_pairs']]),
                    'regression_pairs': '; '.join([f"({a},{b})" for a, b in distances['regression_pairs']]),
                    
                    # Word-level counts and rates
                    'skipped_words_count': len(distances['skipped_words']),
                    'regressed_words_count': len(distances['regressed_words']),
                    'word_skip_rate': len(distances['skipped_words']) / len(sentence['words']) if len(sentence['words']) > 0 else 0,
                    'word_regression_rate': len(distances['regressed_words']) / len(sentence['words']) if len(sentence['words']) > 0 else 0,
                    
                    # Maximum distances
                    'max_skip_distance': distances['max_skip_distance'],
                    'max_regression_distance': distances['max_regression_distance'],
                }
                
                # Add original fixation-based metrics
                for key, value in sentence['sentence_metrics'].items():
                    if key in ['omission_rate', 'regression_rate']:
                        try:
                            # Rename to clarify these are fixation-based
                            new_key = 'fixation_' + key
                            metrics[new_key] = float(value)
                        except (ValueError, TypeError):
                            metrics[new_key] = None
                
                # Add word-level mean metrics
                for metric, values in word_metrics.items():
                    metrics[f'mean_{metric}'] = safe_mean(values)
                
                sentence_metrics.append(metrics)
                
                # Extract and save fixation sequence
                fixations = extract_fixation_sequence(sentence)
                if fixations:
                    save_fixation_data(participant_id, sentence['sentence_id'], 
                                     fixations, fixations_output_dir)
                
            except Exception as e:
                print(f"Error processing sentence {sentence.get('sentence_id', 'unknown')}: {str(e)}")
                continue
        
        return pd.DataFrame(sentence_metrics)
    
    except Exception as e:
        print(f"Error reading JSON file {json_file}: {str(e)}")
        raise

def calculate_participant_metrics(df):
    """Calculate mean and std metrics for a participant"""
    metrics = {}
    
    # List of metrics to calculate mean and std for
    metric_columns = [
        'fixation_omission_rate', 'fixation_regression_rate',  # Original fixation-based metrics
        'word_skip_rate', 'word_regression_rate',              # New word-based metrics
        'skipped_words_count', 'regressed_words_count',        # Raw counts
        'max_skip_distance', 'max_regression_distance',        # Distances
        'mean_FFD', 'mean_GD', 'mean_GPT', 'mean_TRT',        # Eye-tracking metrics
        'mean_nFixations', 'mean_meanPupilSize',
        'sentence_length'                                      # Sentence info
    ]
    
    for col in metric_columns:
        if col in df.columns:
            try:
                metrics[f'{col}_mean'] = df[col].mean()
                metrics[f'{col}_std'] = df[col].std()
            except Exception as e:
                print(f"Error calculating statistics for {col}: {str(e)}")
                metrics[f'{col}_mean'] = None
                metrics[f'{col}_std'] = None
    
    return metrics

def main():
    # Input and output directories
    input_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_extracted_task2_NR_ET"
    metrics_output_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_processed_task2_NR_ET"
    fixations_output_dir = "/home/baiy4/ScanDL/scripts/data/zuco/fix8_fixations"
    
    # Create output directories if they don't exist
    os.makedirs(metrics_output_dir, exist_ok=True)
    os.makedirs(fixations_output_dir, exist_ok=True)
    
    # Find all JSON files
    json_files = glob(os.path.join(input_dir, "*_NR_processed.json"))
    
    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return
    
    print(f"Found {len(json_files)} JSON files to process")
    
    # Process each participant's data
    all_participant_metrics = []
    all_sentences_data = []  # Store all sentences from all participants
    
    for json_file in json_files:
        try:
            # Extract participant ID
            participant_id = os.path.basename(json_file).replace('_NR_processed.json', '')
            print(f"\nProcessing participant {participant_id}...")
            
            # Process the JSON file
            df = process_participant_json(json_file, metrics_output_dir, fixations_output_dir)
            
            if df.empty:
                print(f"No valid data found for participant {participant_id}")
                continue
            
            # Save sentence-level metrics to CSV
            output_file = os.path.join(metrics_output_dir, f"{participant_id}_sentence_metrics.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved sentence-level metrics to {output_file}")
            
            # Add to all sentences dataset
            all_sentences_data.append(df)
            
            # Calculate and store participant-level metrics
            participant_metrics = calculate_participant_metrics(df)
            participant_metrics['participant_id'] = participant_id
            all_participant_metrics.append(participant_metrics)
            
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
            continue
    
    # Create and save the participant-wise metrics DataFrame
    if all_participant_metrics:
        overall_df = pd.DataFrame(all_participant_metrics)
        overall_output_file = os.path.join(metrics_output_dir, "12_participants_wise_metrics.csv")
        overall_df.to_csv(overall_output_file, index=False)
        print(f"\nSaved participant-wise metrics to {overall_output_file}")
        
        # Print summary statistics
        print("\nSummary of participant-wise metrics:")
        print(overall_df.describe())
    else:
        print("\nNo valid participant metrics were calculated")
    
    # Create and save the aggregated sentences dataset
    if all_sentences_data:
        # Concatenate all sentences from all participants
        all_sentences_df = pd.concat(all_sentences_data, ignore_index=True)
        
        # Save the aggregated dataset
        aggregated_output_file = os.path.join(metrics_output_dir, "all_sentences_aggregated.csv")
        all_sentences_df.to_csv(aggregated_output_file, index=False)
        print(f"\nSaved aggregated sentences dataset to {aggregated_output_file}")
        
        # Calculate overall metrics from the aggregated dataset
        overall_metrics = {}
        
        # Updated list of numeric metrics
        metric_columns = [
            'fixation_omission_rate', 'fixation_regression_rate',  # Original fixation-based metrics
            'word_skip_rate', 'word_regression_rate',              # New word-based metrics
            'skipped_words_count', 'regressed_words_count',        # Raw counts
            'max_skip_distance', 'max_regression_distance',        # Distances
            'mean_FFD', 'mean_GD', 'mean_GPT', 'mean_TRT',        # Eye-tracking metrics
            'mean_nFixations', 'mean_meanPupilSize'
        ]
        
        # Calculate means and stds for numeric columns
        for col in metric_columns:
            if col in all_sentences_df.columns:
                try:
                    overall_metrics[f'{col}_mean'] = all_sentences_df[col].mean()
                    overall_metrics[f'{col}_std'] = all_sentences_df[col].std()
                except Exception as e:
                    print(f"Error calculating statistics for {col}: {str(e)}")
                    overall_metrics[f'{col}_mean'] = None
                    overall_metrics[f'{col}_std'] = None
        
        # Add metadata
        overall_metrics['total_sentences'] = len(all_sentences_df)
        overall_metrics['total_participants'] = all_sentences_df['participant_id'].nunique()
        
        # Add sentence length statistics
        overall_metrics['min_sentence_length'] = all_sentences_df['sentence_length'].min()
        overall_metrics['max_sentence_length'] = all_sentences_df['sentence_length'].max()
        overall_metrics['mean_sentence_length'] = all_sentences_df['sentence_length'].mean()
        overall_metrics['std_sentence_length'] = all_sentences_df['sentence_length'].std()
        
        # Save overall metrics to a separate file
        overall_metrics_df = pd.DataFrame([overall_metrics])
        overall_metrics_file = os.path.join(metrics_output_dir, "overall_metrics.csv")
        overall_metrics_df.to_csv(overall_metrics_file, index=False)
        print(f"\nSaved overall metrics to {overall_metrics_file}")
        
        # Print summary statistics for the aggregated dataset
        print("\nSummary of aggregated sentences dataset:")
        print(f"Total number of sentences: {len(all_sentences_df)}")
        print(f"Number of unique participants: {all_sentences_df['participant_id'].nunique()}")
        print("\nMetrics summary:")
        print(all_sentences_df[metric_columns].describe())
    else:
        print("\nNo valid sentences data to aggregate")

if __name__ == "__main__":
    main()
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
    # Filter out None values
    valid_values = [v for v in values if v is not None]
    if not valid_values:
        return None
    return np.mean(valid_values)

def process_participant_json(json_file):
    """Process a single participant's JSON file and return a DataFrame with sentence-level metrics"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract participant ID from filename
    participant_id = os.path.basename(json_file).replace('_NR_processed.json', '')
    
    # Create a list to store sentence-level metrics
    sentence_metrics = []
    
    for sentence in data:
        # Extract word-level metrics safely
        ffd_values = [word['metrics']['FFD'] for word in sentence['words']]
        gd_values = [word['metrics']['GD'] for word in sentence['words']]
        gpt_values = [word['metrics']['GPT'] for word in sentence['words']]
        trt_values = [word['metrics']['TRT'] for word in sentence['words']]
        nfix_values = [word['metrics']['nFixations'] for word in sentence['words']]
        pupil_values = [word['metrics']['meanPupilSize'] for word in sentence['words']]
        
        metrics = {
            'participant_id': participant_id,
            'sentence_id': sentence['sentence_id'],
            'sentence_content': sentence['sentence_content'],
            'omission_rate': sentence['sentence_metrics']['omission_rate'],
            'skip_rate': sentence['sentence_metrics']['skip_rate'],
            'revisit_rate': sentence['sentence_metrics']['revisit_rate'],
            'regression_rate': sentence['sentence_metrics']['regression_rate'],
            'total_fixations': sentence['sentence_metrics']['total_fixations'],
            'skipped_words': sentence['sentence_metrics']['skipped_words'],
            'revisited_words': sentence['sentence_metrics']['revisited_words'],
            'regressions': sentence['sentence_metrics']['regressions'],
            'total_words': len(sentence['words']),
            'mean_FFD': safe_mean(ffd_values),
            'mean_GD': safe_mean(gd_values),
            'mean_GPT': safe_mean(gpt_values),
            'mean_TRT': safe_mean(trt_values),
            'mean_nFixations': safe_mean(nfix_values),
            'mean_pupil_size': safe_mean(pupil_values)
        }
        sentence_metrics.append(metrics)
    
    return pd.DataFrame(sentence_metrics)

def calculate_participant_metrics(df):
    """Calculate mean and std metrics for a participant"""
    metrics = {}
    
    # List of metrics to calculate mean and std for
    metric_columns = [
        'omission_rate', 'skip_rate', 'revisit_rate', 'regression_rate',
        'total_fixations', 'skipped_words', 'revisited_words', 'regressions',
        'mean_FFD', 'mean_GD', 'mean_GPT', 'mean_TRT', 'mean_nFixations',
        'mean_pupil_size'
    ]
    
    for col in metric_columns:
        if col in df.columns:
            metrics[f'{col}_mean'] = df[col].mean()
            metrics[f'{col}_std'] = df[col].std()
    
    return metrics

def main():
    # Input and output directories
    input_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_processed_fixations_task2_NR_ET"
    output_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_processed_task2_NR_ET"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all JSON files
    json_files = glob(os.path.join(input_dir, "*_NR_processed.json"))
    
    # Process each participant's data
    all_participant_metrics = []
    
    for json_file in json_files:
        try:
            # Extract participant ID
            participant_id = os.path.basename(json_file).replace('_NR_processed.json', '')
            print(f"Processing participant {participant_id}...")
            
            # Process the JSON file
            df = process_participant_json(json_file)
            
            # Save sentence-level metrics to CSV
            output_file = os.path.join(output_dir, f"{participant_id}_sentence_metrics.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved sentence-level metrics to {output_file}")
            
            # Calculate and store participant-level metrics
            participant_metrics = calculate_participant_metrics(df)
            participant_metrics['participant_id'] = participant_id
            all_participant_metrics.append(participant_metrics)
            
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
            continue
    
    # Create and save the overall metrics DataFrame
    if all_participant_metrics:
        overall_df = pd.DataFrame(all_participant_metrics)
        overall_output_file = os.path.join(output_dir, "overall_participant_metrics.csv")
        overall_df.to_csv(overall_output_file, index=False)
        print(f"Saved overall participant metrics to {overall_output_file}")
        
        # Print summary statistics
        print("\nSummary of participant metrics:")
        print(overall_df.describe())

if __name__ == "__main__":
    main()
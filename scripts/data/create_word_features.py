import pandas as pd
import json
from typing import Dict, List
import os

def create_word_features(input_path: str, output_path: str):
    """Create word features JSON from complete word analysis CSV"""
    # Read CSV
    df = pd.read_csv(input_path)
    
    # Create word features dictionary
    word_features = {}
    sentence_info = {}
    
    # Process each word
    for _, row in df.iterrows():
        word = row['word']
        sentence_id = row['sentence_id']
        word_id = row['word_id']
        
        # Add word features
        word_features[word] = {
            'length': row['length'],
            'frequency': row['frequency'],
            'log_frequency': row['log_frequency'],
            'difficulty': row['difficulty'],
            'predictability': row['predictability']
        }
        
        # Add sentence information
        if sentence_id not in sentence_info:
            sentence_info[sentence_id] = {
                'sentence': row['sentence'],
                'words': []
            }
        
        # Add word to sentence
        sentence_info[sentence_id]['words'].append({
            'word': word,
            'word_id': word_id,
            'word_clean': row['word_clean']
        })
    
    # Create final dataset structure
    dataset = {
        'word_features': word_features,
        'sentences': sentence_info
    }
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\nWord Features Summary:")
    print(f"Total words: {len(word_features)}")
    print(f"Total sentences: {len(sentence_info)}")
    print(f"Average word length: {df['length'].mean():.2f}")
    print(f"Average word frequency: {df['frequency'].mean():.2f}")
    print(f"Average word difficulty: {df['difficulty'].mean():.2f}")
    print(f"Average word predictability: {df['predictability'].mean():.2f}")

if __name__ == "__main__":
    # Define paths
    input_path = "/home/baiy4/ScanDL/scripts/data/zuco/bai_word_probability_analysis/complete_word_analysis.csv"
    output_path = "/home/baiy4/ScanDL/scripts/data/zuco/bai_word_probability_analysis/word_features.json"
    
    # Create word features
    create_word_features(input_path, output_path) 
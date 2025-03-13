import pandas as pd
import numpy as np
from collections import defaultdict
import json
import os
from typing import Dict, List, Tuple

def calculate_word_difficulty(freq_per_million: float, alpha: float = 1.0, beta: float = 1.0, F: float = 11.0) -> float:
    """Calculate word difficulty based on SWIFT model"""
    if freq_per_million <= 0:
        return alpha
    log_freq = np.log10(freq_per_million)
    difficulty = alpha * (1 - beta * (log_freq / F))
    return max(0, difficulty)

def clean_word(word: str) -> str:
    """Clean a word by removing punctuation and converting to lowercase"""
    # Remove punctuation and convert to lowercase
    word = ''.join(c.lower() for c in word if c.isalnum())
    return word

def load_word_features(word_features_path: str) -> Dict[str, Dict]:
    """Load pre-computed word features from JSON file"""
    with open(word_features_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_sentence(sentence: str, word_features: Dict[str, Dict]) -> Tuple[List[Dict], Dict]:
    """Process a single sentence to extract word and sentence features"""
    words = sentence.split()
    word_data = []
    
    # Track sentence-level statistics
    sentence_stats = {
        'total_words': len(words),
        'avg_word_length': 0,
        'avg_word_frequency': 0,
        'avg_word_difficulty': 0,
        'avg_word_predictability': 0,
        'max_word_length': 0,
        'min_word_length': float('inf'),
        'max_word_difficulty': 0,
        'min_word_difficulty': float('inf'),
        'max_word_predictability': 0,
        'min_word_predictability': float('inf')
    }
    
    # Process each word
    for word in words:
        clean_word_text = clean_word(word)
        
        # Get word features
        features = word_features.get(clean_word_text, {
            'length': len(clean_word_text),
            'frequency': 1.0,
            'log_frequency': 0.0,
            'difficulty': calculate_word_difficulty(1.0),
            'predictability': 0.0001
        })
        
        # Create word data
        word_data.append({
            'word': word,
            'word_clean': clean_word_text,
            'length': features['length'],
            'frequency': features['frequency'],
            'log_frequency': features['log_frequency'],
            'difficulty': features['difficulty'],
            'predictability': features['predictability']
        })
        
        # Update sentence statistics
        sentence_stats['avg_word_length'] += features['length']
        sentence_stats['avg_word_frequency'] += features['frequency']
        sentence_stats['avg_word_difficulty'] += features['difficulty']
        sentence_stats['avg_word_predictability'] += features['predictability']
        
        sentence_stats['max_word_length'] = max(sentence_stats['max_word_length'], features['length'])
        sentence_stats['min_word_length'] = min(sentence_stats['min_word_length'], features['length'])
        sentence_stats['max_word_difficulty'] = max(sentence_stats['max_word_difficulty'], features['difficulty'])
        sentence_stats['min_word_difficulty'] = min(sentence_stats['min_word_difficulty'], features['difficulty'])
        sentence_stats['max_word_predictability'] = max(sentence_stats['max_word_predictability'], features['predictability'])
        sentence_stats['min_word_predictability'] = min(sentence_stats['min_word_predictability'], features['predictability'])
    
    # Calculate averages
    n_words = len(words)
    sentence_stats['avg_word_length'] /= n_words
    sentence_stats['avg_word_frequency'] /= n_words
    sentence_stats['avg_word_difficulty'] /= n_words
    sentence_stats['avg_word_predictability'] /= n_words
    
    return word_data, sentence_stats

def create_sentence_dataset(sentences_path: str, word_features_path: str, output_path: str):
    """Create a dataset of sentences with word features for reinforcement learning training"""
    # Load sentences
    sentences_df = pd.read_csv(sentences_path)
    
    # Load word features
    word_features = load_word_features(word_features_path)
    
    # Process each sentence
    dataset = []
    for _, row in sentences_df.iterrows():
        sentence_id = row['sentence_id']
        sentence = row['sentence']
        
        # Process sentence
        word_data, sentence_stats = process_sentence(sentence, word_features)
        
        # Create sentence entry
        sentence_entry = {
            'sentence_id': sentence_id,
            'sentence': sentence,
            'sentence_stats': sentence_stats,
            'words': word_data
        }
        
        dataset.append(sentence_entry)
    
    # Save dataset
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    # Print summary statistics
    print(f"\nDataset Summary:")
    print(f"Total sentences: {len(dataset)}")
    print(f"Total unique words: {len(word_features)}")
    print("\nSentence Statistics:")
    print(f"Average words per sentence: {np.mean([len(s['words']) for s in dataset]):.2f}")
    print(f"Average word length: {np.mean([s['sentence_stats']['avg_word_length'] for s in dataset]):.2f}")
    print(f"Average word difficulty: {np.mean([s['sentence_stats']['avg_word_difficulty'] for s in dataset]):.2f}")
    print(f"Average word predictability: {np.mean([s['sentence_stats']['avg_word_predictability'] for s in dataset]):.2f}")

if __name__ == "__main__":
    # Define paths
    sentences_path = "/home/baiy4/ScanDL/scripts/data/zuco/task_materials/relations_labels_task2.csv"
    word_features_path = "/home/baiy4/ScanDL/scripts/data/zuco/bai_word_probability_analysis/word_features.json"
    output_path = "/home/baiy4/ScanDL/scripts/data/zuco/bai_word_probability_analysis/sentence_dataset.json"
    
    # Create dataset
    create_sentence_dataset(sentences_path, word_features_path, output_path) 
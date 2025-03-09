import json
import os
import numpy as np
from glob import glob
from collections import defaultdict

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
        'skipped_words': set(),       # Words skipped during first-pass reading
        'regressed_words': set(),     # Words that were regressed to
        'skip_pairs': [],            # List of (from, to) pairs for first-pass skips
        'regression_pairs': [],      # List of (from, to) pairs for regressions
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
    max_word_seen = word_sequence[0]      # Tracks furthest word seen in first pass
    current_word = word_sequence[0]       # Current word being processed
    first_pass_words = {word_sequence[0]} # Words seen in first pass
    seen_words = {word_sequence[0]}      # All words that have been fixated
    
    # Process the sequence
    for i in range(1, len(word_sequence)):
        prev_word = current_word
        current_word = word_sequence[i]
        
        # Check if current word is in first pass (i.e., not seen before)
        is_current_first_pass = current_word not in seen_words
        
        if current_word > prev_word:
            # Forward reading
            if current_word - prev_word > 1:
                # Check if this is a valid skip:
                # 1. Both words are in first pass, or
                # 2. Landing word (current_word) is in first pass
                if (prev_word in first_pass_words and is_current_first_pass) or is_current_first_pass:
                    distances['skip_pairs'].append((prev_word, current_word))
                    # Add skipped words
                    for skipped_idx in range(prev_word + 1, current_word):
                        distances['skipped_words'].add(skipped_idx)
            
            # Update max_word_seen and first_pass_words
            if current_word > max_word_seen:
                max_word_seen = current_word
            if is_current_first_pass:
                first_pass_words.add(current_word)
                
        elif current_word < prev_word:
            # Regression detected
            regression_distance = prev_word - current_word
            if regression_distance <= 5:  # Only count short-distance regressions
                distances['regression_pairs'].append((prev_word, current_word))
                distances['regressed_words'].add(current_word)
        
        seen_words.add(current_word)
    
    return distances

def calculate_word_difficulty(freq_per_million, alpha=1.0, beta=1.0, F=11):
    """
    Calculate word difficulty based on SWIFT model
    Ln = α(1 - β(log fn/F))
    
    Args:
        freq_per_million: word frequency per million
        alpha: intercept value of lexical access time
        beta: slope parameter
        F: scaling constant (default 11)
    """
    if freq_per_million <= 0:
        return alpha  # Maximum difficulty for unknown words
    
    log_freq = np.log10(freq_per_million)  # Use log10 to match the paper
    difficulty = alpha * (1 - beta * (log_freq / F))
    return max(0, difficulty)  # Ensure non-negative difficulty

def analyze_sentence_words(sentence, word_frequencies):
    """
    Analyze words in a sentence and their features
    """
    words = sentence['words']
    word_data = []
    
    for i, word in enumerate(words):
        # Get word content from the correct field
        word_text = word['content'].lower()  # Convert to lowercase
        
        # Get frequency info
        freq_info = word_frequencies.get(word_text, {
            'freq_per_million': 1.0,
            'log_freq_per_million': 0.0,
            'contextual_diversity': 0,
            'cd_percent': 0.0,
            'length': len(word_text)
        })
        
        # Calculate word difficulty using SWIFT model
        difficulty = calculate_word_difficulty(
            freq_info['freq_per_million'],
            alpha=1.0,  # These parameters can be tuned
            beta=1.0,
            F=11
        )
        
        # Create word info dictionary with all available metrics
        word_info = {
            'word': word_text,
            'index': i,
            'length': len(word_text),
            # Frequency metrics
            'frequency_per_million': freq_info['freq_per_million'],
            'log_frequency': freq_info['log_freq_per_million'],
            'contextual_diversity': freq_info.get('contextual_diversity', 0),
            'cd_percent': freq_info.get('cd_percent', 0.0),
            # Word difficulty (SWIFT model)
            'difficulty': difficulty,
            # Predictability (placeholder)
            'predictability': 0.0,  # To be filled later with LLM
            'log_predictability': 0.0,  # log10 of predictability
            # Eye-tracking metrics
            'FFD': word['metrics'].get('FFD'),
            'GD': word['metrics'].get('GD'),
            'GPT': word['metrics'].get('GPT'),
            'TRT': word['metrics'].get('TRT'),
            'nFixations': word['metrics'].get('nFixations'),
            'meanPupilSize': word['metrics'].get('meanPupilSize'),
            # Word status
            'skipped': word.get('skipped', False),
            'revisited': word.get('revisited', False)
        }
        word_data.append(word_info)
    
    return word_data

def create_word_feature_analysis(input_json, word_frequencies_file, output_file):
    """
    Create analysis JSON file with word features for skipped and regressed words
    """
    # Load word frequencies
    with open(word_frequencies_file, 'r', encoding='utf-8') as f:
        word_frequencies = json.load(f)
    
    # Load input data
    with open(input_json, 'r', encoding='utf-8') as f:
        sentences = json.load(f)
    
    analyses = []
    
    for sentence in sentences:
        try:
            # Get word features for all words
            word_data = analyze_sentence_words(sentence, word_frequencies)
            
            # Calculate distances to get skipped and regressed words
            distances = calculate_distances(sentence)
            
            # Create analysis entry
            analysis = {
                'sentence_id': sentence['sentence_id'],
                'sentence_content': sentence['sentence_content'],
                'sentence_metrics': sentence.get('sentence_metrics', {}),
                'words': word_data,  # Store all words and their features
                'skipped_words': [],
                'regressed_words': []
            }
            
            # Add skipped words and their features
            for word_idx in distances['skipped_words']:
                if 0 <= word_idx < len(word_data):
                    analysis['skipped_words'].append(word_data[word_idx])
            
            # Add regressed words and their features
            for word_idx in distances['regressed_words']:
                if 0 <= word_idx < len(word_data):
                    analysis['regressed_words'].append(word_data[word_idx])
            
            analyses.append(analysis)
            
        except Exception as e:
            print(f"Error processing sentence {sentence.get('sentence_id', 'unknown')}: {str(e)}")
            continue
    
    # Save to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analyses, f, indent=2)
    
    # Print some statistics
    total_words = sum(len(analysis['words']) for analysis in analyses)
    total_skipped = sum(len(analysis['skipped_words']) for analysis in analyses)
    total_regressed = sum(len(analysis['regressed_words']) for analysis in analyses)
    
    print(f"\nAnalysis statistics for {output_file}:")
    print(f"Total sentences: {len(analyses)}")
    print(f"Total words: {total_words}")
    print(f"Total skipped words: {total_skipped} ({total_skipped/total_words*100:.1f}%)")
    print(f"Total regressed words: {total_regressed} ({total_regressed/total_words*100:.1f}%)")

def main():
    # Paths
    input_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_extracted_task2_NR_ET"
    output_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_analyzed_word_features_on_word_skipping_and_regression"
    word_frequencies_file = "/home/baiy4/ScanDL/scripts/data/word_frequencies.json"  # You'll need to provide this
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each participant's file
    for json_file in glob(os.path.join(input_dir, "*_NR_processed.json")):
        try:
            participant_id = os.path.basename(json_file).replace('_NR_processed.json', '')
            output_file = os.path.join(output_dir, f"{participant_id}_word_features.json")
            
            create_word_feature_analysis(json_file, word_frequencies_file, output_file)
            print(f"Processed participant {participant_id}")
            
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

if __name__ == "__main__":
    main() 
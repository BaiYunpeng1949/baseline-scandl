import json
import os
import numpy as np
from glob import glob
import string

def clean_word(word):
    """Clean word by removing punctuation and converting to lowercase"""
    # Remove punctuation from start and end of word
    word = word.lower().strip()
    # Remove all punctuation marks
    word = ''.join(char for char in word if char not in string.punctuation)
    return word

def calculate_word_difficulty(freq_per_million, alpha=1.0, beta=1.0, F=11):
    """Calculate word difficulty based on SWIFT model"""
    if freq_per_million <= 0:
        return alpha
    log_freq = np.log10(freq_per_million)
    difficulty = alpha * (1 - beta * (log_freq / F))
    return max(0, difficulty)

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

def analyze_sentence_reading_patterns(sentence, word_frequencies, word_predictabilities):
    """Analyze reading patterns for a single sentence"""
    # First, get the fixation sequence
    fixation_sequence = []
    for fix in sentence['fixation_sequence']:
        fixation_sequence.append(fix['word_idx'])
    
    # Normalize the sequence
    word_sequence = normalize_reading_sequence(fixation_sequence)
    
    if not word_sequence:
        return None
    
    # Initialize tracking variables
    max_word_seen = word_sequence[0]      # Tracks furthest word seen in first pass
    current_word = word_sequence[0]       # Current word being processed
    first_pass_words = {word_sequence[0]} # Words seen in first pass
    seen_words = {word_sequence[0]}      # All words that have been fixated
    
    # Track skipped and regressed words
    skipped_words = set()
    regressed_words = set()
    
    # Process the sequence
    for i in range(1, len(word_sequence)):
        prev_word = current_word
        current_word = word_sequence[i]
        
        # Check if current word is in first pass
        is_current_first_pass = current_word not in seen_words
        
        if current_word > prev_word:
            # Forward reading
            if current_word - prev_word > 1:
                # Words were skipped
                if (prev_word in first_pass_words and is_current_first_pass) or is_current_first_pass:
                    for skipped_idx in range(prev_word + 1, current_word):
                        skipped_words.add(skipped_idx)
            
            # Update max_word_seen and first_pass_words
            if current_word > max_word_seen:
                max_word_seen = current_word
            if is_current_first_pass:
                first_pass_words.add(current_word)
                
        elif current_word < prev_word:
            # Regression detected
            regression_distance = prev_word - current_word
            if regression_distance <= 5:  # Only count short-distance regressions
                regressed_words.add(current_word)
        
        seen_words.add(current_word)
    
    # Get predictability data for this sentence
    sentence_predictabilities = word_predictabilities.get(str(sentence['sentence_id']), {})
    word_preds = sentence_predictabilities.get('word_predictabilities', [])
    word_logit_preds = sentence_predictabilities.get('word_logit_predictabilities', [])
    
    # Analyze each word
    analyzed_words = []
    for word_idx, word_info in enumerate(sentence['words']):
        # Get original and cleaned word text
        original_word = word_info['content']
        word_text = clean_word(original_word)
        word_idx = word_info['word_id']
        
        # Get word frequency info
        freq_info = word_frequencies.get(word_text, {
            'freq_per_million': 1.0,
            'log_freq_per_million': 0.0
        })
        
        # Get word predictability and logit predictability
        predictability = word_preds[word_idx] if word_idx < len(word_preds) else 0.0
        logit_predictability = word_logit_preds[word_idx] if word_idx < len(word_logit_preds) else -2.553  # Default to lowest class
        
        # Calculate word features
        analyzed_word = {
            'word': original_word,  # Keep original word for reference
            'word_clean': word_text,  # Store cleaned word
            'word_id': word_idx,
            'length': len(word_text),  # Use cleaned word length
            'frequency_per_million': freq_info.get('freq_per_million', 1.0),
            'log_frequency': freq_info.get('log_freq_per_million', 0.0),
            'difficulty': calculate_word_difficulty(freq_info.get('freq_per_million', 1.0)),
            'predictability': predictability,  # Raw predictability
            'logit_predictability': logit_predictability,  # Logit transformed predictability
            
            # Reading behavior
            'is_first_pass_skip': word_idx in skipped_words,
            'is_regression_target': word_idx in regressed_words,
            
            # Original eye-tracking metrics (for reference)
            'FFD': word_info['metrics']['FFD'],
            'GD': word_info['metrics']['GD'],
            'TRT': word_info['metrics']['TRT'],
            'nFixations': word_info['metrics']['nFixations']
        }
        
        analyzed_words.append(analyzed_word)
    
    return {
        'sentence_id': sentence['sentence_id'],
        'sentence_content': sentence['sentence_content'],
        'words': analyzed_words
    }

def process_participant_data(input_file, word_frequencies_file, word_predictabilities_file, output_file):
    """Process a single participant's data"""
    # Load word frequencies
    with open(word_frequencies_file, 'r', encoding='utf-8') as f:
        word_frequencies = json.load(f)
    
    # Load word predictabilities
    with open(word_predictabilities_file, 'r', encoding='utf-8') as f:
        word_predictabilities = json.load(f)
    
    # Load participant data
    with open(input_file, 'r', encoding='utf-8') as f:
        sentences = json.load(f)
    
    # Process each sentence
    analyzed_sentences = []
    for sentence in sentences:
        try:
            analyzed = analyze_sentence_reading_patterns(sentence, word_frequencies, word_predictabilities)
            analyzed_sentences.append(analyzed)
        except Exception as e:
            print(f"Error processing sentence {sentence.get('sentence_id', 'unknown')}: {str(e)}")
            continue
    
    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analyzed_sentences, f, indent=2)

def main():
    # Paths
    input_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_extracted_task2_NR_ET"
    output_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_reading_pattern_analysis"
    word_frequencies_file = "/home/baiy4/ScanDL/scripts/data/word_frequencies.json"
    word_predictabilities_file = "/home/baiy4/ScanDL/scripts/data/word_predictabilities.json"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each participant's file
    for input_file in glob(os.path.join(input_dir, "*_NR_processed.json")):
        try:
            participant_id = os.path.basename(input_file).replace('_NR_processed.json', '')
            output_file = os.path.join(output_dir, f"{participant_id}_reading_patterns.json")
            
            print(f"Processing participant {participant_id}...")
            process_participant_data(input_file, word_frequencies_file, word_predictabilities_file, output_file)
            print(f"Completed processing {participant_id}")
            
            # Print some statistics from the first file
            if participant_id == os.path.basename(glob(os.path.join(input_dir, "*_NR_processed.json"))[0]).replace('_NR_processed.json', ''):
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_words = sum(len(sent['words']) for sent in data)
                    skipped_words = sum(
                        sum(1 for word in sent['words'] if word['is_first_pass_skip'])
                        for sent in data
                    )
                    regressed_words = sum(
                        sum(1 for word in sent['words'] if word['is_regression_target'])
                        for sent in data
                    )
                    avg_predictability = np.mean([
                        word['predictability']
                        for sent in data
                        for word in sent['words']
                    ])
                    print(f"\nExample statistics for {participant_id}:")
                    print(f"Total words: {total_words}")
                    print(f"First-pass skipped words: {skipped_words} ({skipped_words/total_words*100:.1f}%)")
                    print(f"Regression targets: {regressed_words} ({regressed_words/total_words*100:.1f}%)")
                    print(f"Average word predictability: {avg_predictability:.3f}")
        
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")

if __name__ == "__main__":
    main() 
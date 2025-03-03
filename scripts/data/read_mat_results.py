import scipy.io as io
import os
import json
import numpy as np
from utils_ZuCo import DataTransformer

# # Create a DataTransformer instance
# # task1 = Natural Reading (NR)
# # You can choose level='sentence' or level='word'
# # scaling and fillna are optional parameters with defaults
# transformer = DataTransformer(
#     task='task1',  # For Natural Reading task
#     level='word',  # To see word-level data
#     scaling='raw', # To see raw values without normalization
#     fillna='zeros' # How to handle missing values
# )

# # ZAB is subject 0 in the dataset
# zab_data = transformer(subject=0)

# # Now you can examine the data
# print(zab_data.head())  # Show first few rows
# print(zab_data.columns) # Show all available features

# Direct path to ZAB's result file
path = "/home/baiy4/ScanDL/scripts/data/zuco/task2/Matlab_files/"  # Adjust this path to where your files are
file_path = os.path.join(path, "resultsZAB_NR.mat")

# Load the mat file with squeeze_me=True and struct_as_record=False for better handling
mat_data = io.loadmat(file_path, squeeze_me=True, struct_as_record=False)

# 1. First, let's look at the keys
print("Keys in the .mat file:")
print(mat_data.keys())

# 2. Look at the sentenceData structure
sentence_data = mat_data['sentenceData']
print("\nShape of sentenceData:")
print(sentence_data.shape)

# 3. Look at the first sentence's data
first_sentence = sentence_data[0]
print("\nAttributes of first sentence:")
for attr in dir(first_sentence):
    if not attr.startswith('_'):  # Skip private attributes
        try:
            value = getattr(first_sentence, attr)
            if not callable(value):  # Skip methods, only show data
                print(f"{attr}: {value}")
        except:
            print(f"{attr}: <unable to display>")

# 4. Look at word-level data for the first sentence
print("\nFirst sentence words:")
for i, word in enumerate(first_sentence.word):
    print(f"\nWord {i}:")
    print(f"Content: {word.content}")
    print(f"FFD (First Fixation Duration): {word.FFD}")
    print(f"TRT (Total Reading Time): {word.TRT}")
    print(f"Number of fixations: {word.nFixations}")
    # Only show first 3 words
    if i >= 2:
        print("...")
        break

# Print all top-level keys and their structure
# Look at what's in the data
print(f"the mat data looks like this: {mat_data}")

# The actual data is in 'sentenceData'
sentence_data = mat_data['sentenceData']

# Print information about the first sentence
print("\nFirst sentence information:")
first_sentence = sentence_data[0]
# print(f"Content: {first_sentence.content}")

# Print available attributes of the first sentence
print("\nAvailable attributes for each sentence:")
print([attr for attr in dir(first_sentence) if not attr.startswith('_')])

# # Look at word-level data for the first sentence
# print("\nFirst word information:")
# # first_word = first_sentence.word[0]
# # print(f"Word content: {first_word.content}")

# # Print some example metrics for the first word
# print("\nExample metrics for first word:")
# print(f"First fixation duration (FFD): {first_word.FFD}")
# print(f"Total reading time (TRT): {first_word.TRT}")
# print(f"Number of fixations: {first_word.nFixations}")

def convert_to_serializable(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

# Create the data structure
zuco_data = []

# Iterate through sentences
for sent_idx, sentence in enumerate(sentence_data):
    sentence_obj = {
        "sentence_id": sent_idx,
        "sentence_content": sentence.content,
        "sentence_metrics": {
            "omission_rate": convert_to_serializable(sentence.omissionRate),
        },
        # Add total number of fixations for the sentence
        "total_fixations": len(convert_to_serializable(sentence.allFixations.x)) if hasattr(sentence.allFixations, 'x') else 0,
        "words": [],
        "fixation_sequence": []
    }
    
    # Get all fixation data for this sentence
    all_fixations = {
        'x': convert_to_serializable(sentence.allFixations.x) if hasattr(sentence.allFixations, 'x') else [],
        'y': convert_to_serializable(sentence.allFixations.y) if hasattr(sentence.allFixations, 'y') else [],
        'duration': convert_to_serializable(sentence.allFixations.duration) if hasattr(sentence.allFixations, 'duration') else [],
    }
    
    # Track the global sequence of fixations for regression analysis
    global_fixation_sequence = []
    
    # First pass: Record all fixations in sequence
    for word_idx, word in enumerate(sentence.word):
        if hasattr(word, 'fixPositions') and not (
            not hasattr(word, 'FFD') or 
            (hasattr(word, 'FFD') and (np.size(word.FFD) == 0 or word.FFD == 0)) or 
            not hasattr(word, 'nFixations') or
            (hasattr(word, 'nFixations') and (np.size(word.nFixations) == 0 or word.nFixations == 0))
        ):
            fix_positions = convert_to_serializable(word.fixPositions)
            if isinstance(fix_positions, int):
                fix_positions = [fix_positions]
            
            for pos in fix_positions:
                if pos > 0 and pos-1 < len(all_fixations['x']):
                    global_fixation_sequence.append({
                        'word_idx': word_idx,
                        'global_index': pos-1,
                        'x': all_fixations['x'][pos-1],
                        'y': all_fixations['y'][pos-1],
                        'duration': all_fixations['duration'][pos-1]
                    })

    # Sort fixations by their global_index to ensure chronological order
    global_fixation_sequence.sort(key=lambda x: x['global_index'])
    
    # Add sequence information and detect regressions
    for i in range(len(global_fixation_sequence)):
        global_fixation_sequence[i]['sequence_index'] = i
        if i > 0:
            # Mark as regression if moving left compared to previous fixation
            global_fixation_sequence[i]['is_regression'] = (
                global_fixation_sequence[i]['x'] < global_fixation_sequence[i-1]['x']
            )
        else:
            global_fixation_sequence[i]['is_regression'] = False

    # Add sentence-level fixation sequence
    sentence_obj["fixation_sequence"] = global_fixation_sequence
    
    # Add word-level data
    for word_idx, word in enumerate(sentence.word):
        # Check if word was skipped
        was_skipped = (not hasattr(word, 'FFD') or 
                      (hasattr(word, 'FFD') and (np.size(word.FFD) == 0 or word.FFD == 0)) or 
                      not hasattr(word, 'nFixations') or
                      (hasattr(word, 'nFixations') and (np.size(word.nFixations) == 0 or word.nFixations == 0)))
        
        word_obj = {
            "word_id": word_idx,
            "content": word.content,
            "skipped": was_skipped,
            "metrics": {
                "FFD": convert_to_serializable(word.FFD) if hasattr(word, 'FFD') else None,
                "SFD": convert_to_serializable(word.SFD) if hasattr(word, 'SFD') else None,
                "GD": convert_to_serializable(word.GD) if hasattr(word, 'GD') else None,
                "GPT": convert_to_serializable(word.GPT) if hasattr(word, 'GPT') else None,
                "TRT": convert_to_serializable(word.TRT) if hasattr(word, 'TRT') else None,
                "nFixations": convert_to_serializable(word.nFixations) if hasattr(word, 'nFixations') else 0,
                "meanPupilSize": convert_to_serializable(word.meanPupilSize) if hasattr(word, 'meanPupilSize') else None
            },
            "fixations": {
                "coordinates": [],
                "word_bounds": convert_to_serializable(sentence.wordbounds[word_idx]) if hasattr(sentence, 'wordbounds') else None,
                "has_regression": False  # Will be updated if regressions are found
            }
        }

        # Get fixation positions for this word
        if hasattr(word, 'fixPositions') and not was_skipped:
            fix_positions = convert_to_serializable(word.fixPositions)
            if isinstance(fix_positions, int):
                fix_positions = [fix_positions]
            
            coordinates = []
            for fix_idx, pos in enumerate(fix_positions):
                if pos > 0 and pos-1 < len(all_fixations['x']):
                    coordinates.append({
                        "fixation_index": fix_idx,        # Order within this word
                        "global_index": pos-1,            # Position in sentence
                        "x": all_fixations['x'][pos-1],
                        "y": all_fixations['y'][pos-1],
                        "duration": all_fixations['duration'][pos-1],
                        "is_regression": False            # Will be updated below
                    })
            
            # Detect regressions by comparing x-coordinates
            for i in range(1, len(coordinates)):
                if coordinates[i]["x"] < coordinates[i-1]["x"]:
                    coordinates[i]["is_regression"] = True
            
            word_obj["fixations"]["coordinates"] = coordinates
            word_obj["fixations"]["has_regression"] = any(c["is_regression"] for c in coordinates)
        
        sentence_obj["words"].append(word_obj)
    
    zuco_data.append(sentence_obj)

# Save to JSON file
json_save_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_processed_fixations_task2_NR_ET"
output_path = os.path.join(json_save_dir, "ZAB_NR_processed.json")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(zuco_data, f, indent=2, ensure_ascii=False)

# Print example of first sentence to verify
print("\nExample of first word in first sentence:")
print(json.dumps(zuco_data[0]["words"][0], indent=2))
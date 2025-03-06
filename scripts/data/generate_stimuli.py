import os
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from glob import glob
import scipy.io as io

def load_word_bounds():
    """Load word boundaries from a MATLAB file"""
    # Load from any participant's data as they should all have the same layout
    mat_file = "/home/baiy4/ScanDL/scripts/data/zuco/task2/Matlab_files/resultsZAB_NR.mat"
    mat_data = io.loadmat(mat_file, squeeze_me=True, struct_as_record=False)
    
    # Extract word boundaries for each sentence
    sentence_data = mat_data['sentenceData']
    bounds_data = {}
    
    for sent_idx, sentence in enumerate(sentence_data):
        if hasattr(sentence, 'wordbounds'):
            bounds = sentence.wordbounds
            bounds_data[sent_idx] = bounds
    
    return bounds_data

def get_all_sentences():
    """Get all sentences from the CSV files and assign new sequential IDs"""
    csv_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_processed_task2_NR_ET"
    all_sentences = []
    
    # Read all participant CSV files
    csv_files = glob(os.path.join(csv_dir, "*_sentence_metrics.csv"))
    
    # First, collect all sentences with their original IDs
    original_sentences = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        # Keep track of original sentence_id and content
        sentences = df[['sentence_id', 'sentence_content']].values.tolist()
        original_sentences.extend(sentences)
    
    # Create a mapping from original IDs to new sequential IDs
    unique_pairs = set((orig_id, content) for orig_id, content in original_sentences)
    id_mapping = {}
    for new_id, (orig_id, content) in enumerate(sorted(unique_pairs)):
        id_mapping[(orig_id, content)] = new_id
    
    # Create the final list with new IDs
    for orig_id, content in original_sentences:
        new_id = id_mapping[(orig_id, content)]
        all_sentences.append({
            'new_id': new_id,
            'original_id': orig_id,
            'sentence_content': content
        })
    
    # Sort by new ID
    all_sentences.sort(key=lambda x: x['new_id'])
    
    # Save the ID mapping for reference
    mapping_df = pd.DataFrame([
        {'new_id': new_id, 'original_id': orig_id, 'sentence_content': content}
        for (orig_id, content), new_id in id_mapping.items()
    ])
    mapping_df.sort_values('new_id', inplace=True)
    mapping_df.to_csv("/home/baiy4/ScanDL/scripts/data/zuco/task2_stimuli/id_mapping.csv", index=False)
    
    return all_sentences

def split_sentence_into_lines(sentence, max_chars=80, max_words=13):
    """Split a sentence into lines respecting the maximum characters and words per line"""
    words = sentence.split()
    lines = []
    current_line = []
    current_chars = 0
    current_words = 0
    
    for word in words:
        # Check if adding this word would exceed limits
        if current_words + 1 > max_words or current_chars + len(word) + 1 > max_chars:
            # Save current line and start new one
            lines.append(' '.join(current_line))
            current_line = [word]
            current_chars = len(word)
            current_words = 1
        else:
            # Add word to current line
            current_line.append(word)
            current_chars += len(word) + 1  # +1 for space
            current_words += 1
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def create_stimulus_image(sentence_data, word_bounds, output_dir):
    """Create a stimulus image for a sentence according to specifications"""
    # Image parameters
    bg_color = (211, 211, 211)  # Light grey
    text_color = (0, 0, 0)      # Black
    font_size = 20
    padding = 50
    
    # Get word boundaries for this sentence
    bounds = word_bounds.get(sentence_data['original_id'])
    if bounds is None:
        # Fallback to old method if no bounds found
        return create_stimulus_image_fallback(sentence_data, output_dir)
    
    # Calculate image dimensions based on word boundaries
    min_x = min(bound[0] for bound in bounds)
    max_x = max(bound[2] for bound in bounds)
    min_y = min(bound[1] for bound in bounds)
    max_y = max(bound[3] for bound in bounds)
    
    # Add padding
    img_width = int(max_x - min_x + 2 * padding)
    img_height = int(max_y - min_y + 2 * padding)
    
    # Initialize font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font if Arial is not available
        font = ImageFont.load_default()
    
    # Create image
    img = Image.new('RGB', (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Split sentence into words
    words = sentence_data['sentence_content'].split()
    
    # Draw each word at its exact position
    for word, bound in zip(words, bounds):
        x = bound[0] - min_x + padding
        y = bound[1] - min_y + padding
        draw.text((x, y), word, font=font, fill=text_color)
    
    # Save image
    output_file = os.path.join(output_dir, f"sentence_{sentence_data['new_id']}.png")
    img.save(output_file)
    return output_file

def create_stimulus_image_fallback(sentence_data, output_dir):
    """Fallback method to create stimulus image without word boundaries"""
    # Image parameters
    bg_color = (211, 211, 211)  # Light grey
    text_color = (0, 0, 0)      # Black
    font_size = 20
    line_spacing = font_size * 3  # Triple spacing
    padding = 50
    
    # Initialize font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font if Arial is not available
        font = ImageFont.load_default()
    
    # Split sentence into lines
    lines = split_sentence_into_lines(sentence_data['sentence_content'])
    
    # Calculate image dimensions
    test_img = Image.new('RGB', (1, 1))
    test_draw = ImageDraw.Draw(test_img)
    max_width = max(test_draw.textlength(line, font=font) for line in lines)
    img_width = int(max_width + 2 * padding)
    img_height = int((len(lines) * line_spacing) + 2 * padding)
    
    # Create image
    img = Image.new('RGB', (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw text
    y = padding
    for line in lines:
        draw.text((padding, y), line, font=font, fill=text_color)
        y += line_spacing
    
    # Save image
    output_file = os.path.join(output_dir, f"sentence_{sentence_data['new_id']}.png")
    img.save(output_file)
    return output_file

def main():
    # Set up output directory
    output_dir = "/home/baiy4/ScanDL/scripts/data/zuco/task2_stimuli"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load word boundaries
    print("Loading word boundaries from MATLAB file...")
    word_bounds = load_word_bounds()
    
    # Get all sentences
    print("Loading sentences...")
    sentences = get_all_sentences()
    print(f"Found {len(sentences)} sentences")
    
    # Generate stimuli for each sentence
    for i, sentence_data in enumerate(sentences):
        try:
            output_file = create_stimulus_image(sentence_data, word_bounds, output_dir)
            print(f"Generated stimulus {i+1}/{len(sentences)}: {output_file}")
        except Exception as e:
            print(f"Error generating stimulus for sentence {sentence_data['new_id']}: {str(e)}")
            # Try fallback method
            try:
                output_file = create_stimulus_image_fallback(sentence_data, output_dir)
                print(f"Generated stimulus using fallback method: {output_file}")
            except Exception as e2:
                print(f"Fallback method also failed: {str(e2)}")
    
    print("\nDone! Generated all stimuli images.")
    print(f"A mapping between new IDs and original IDs has been saved to: {output_dir}/id_mapping.csv")

if __name__ == "__main__":
    main()

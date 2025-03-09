import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
from collections import defaultdict
import string

def clean_word(word):
    """Clean word by removing punctuation and converting to lowercase"""
    word = word.lower().strip()
    word = ''.join(char for char in word if char not in string.punctuation)
    return word

def collect_word_statistics():
    """Collect statistics for each unique word across all participants and trials"""
    input_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_reading_pattern_analysis"
    
    # Dictionary to store word statistics
    word_stats = defaultdict(lambda: {
        'total_occurrences': 0,
        'skip_count': 0,
        'regression_count': 0,
        'length': 0,
        'frequency': 0,
        'log_frequency': 0,
        'difficulty': 0,
        'original_forms': set()  # Track original forms of the word
    })
    
    # Process each participant's data
    for file_path in glob(os.path.join(input_dir, "*_reading_patterns.json")):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Process each sentence
                for sentence in data:
                    # Skip None sentences
                    if sentence is None:
                        continue
                        
                    # Skip sentences without words
                    if 'words' not in sentence or not sentence['words']:
                        continue
                        
                    for word_info in sentence['words']:
                        # Get original and cleaned word
                        original_word = word_info['word']  # Original word with punctuation
                        clean_word_text = word_info['word_clean']  # Already cleaned word
                        
                        # Update counts
                        word_stats[clean_word_text]['total_occurrences'] += 1
                        word_stats[clean_word_text]['skip_count'] += 1 if word_info['is_first_pass_skip'] else 0
                        word_stats[clean_word_text]['regression_count'] += 1 if word_info['is_regression_target'] else 0
                        
                        # Update features (will average later)
                        word_stats[clean_word_text]['length'] = len(clean_word_text)  # No need to average length
                        word_stats[clean_word_text]['frequency'] += word_info['frequency_per_million']
                        word_stats[clean_word_text]['log_frequency'] += word_info['log_frequency']
                        word_stats[clean_word_text]['difficulty'] += word_info['difficulty']
                        word_stats[clean_word_text]['original_forms'].add(original_word)
        
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            continue
    
    # Calculate averages and probabilities
    word_data = []
    for word, stats in word_stats.items():
        n = stats['total_occurrences']
        if n > 0:  # Avoid division by zero
            word_data.append({
                'word': word,
                'original_forms': ', '.join(sorted(stats['original_forms'])),
                'length': stats['length'],
                'frequency': stats['frequency'] / n,
                'log_frequency': stats['log_frequency'] / n,
                'difficulty': stats['difficulty'] / n,
                'skip_probability': stats['skip_count'] / n,
                'regression_probability': stats['regression_count'] / n,
                'total_occurrences': n
            })
    
    df = pd.DataFrame(word_data)
    
    # Print some basic statistics
    print(f"\nProcessed {len(word_stats)} unique words")
    print(f"Found {sum(stats['skip_count'] for stats in word_stats.values())} total skips")
    print(f"Found {sum(stats['regression_count'] for stats in word_stats.values())} total regressions")
    
    return df

def analyze_and_plot_relationships(df, output_dir):
    """Analyze relationships and create plots"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style for all plots
    plt.style.use('seaborn-whitegrid')
    
    # Common plot settings
    plot_settings = {
        'figure.figsize': (12, 8),
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12
    }
    plt.rcParams.update(plot_settings)
    
    # 1. Word Length Effect on Skipping
    plt.figure()
    # Create weighted scatter plot based on occurrence count
    sns.scatterplot(data=df, x='length', y='skip_probability', 
                    size='total_occurrences', sizes=(20, 200),
                    alpha=0.3, legend='brief')
    # Add regression line with confidence band
    sns.regplot(data=df, x='length', y='skip_probability', 
                scatter=False,
                line_kws={'linewidth': 2, 'color': 'red'},
                ci=95)
    
    # Add correlation coefficient
    corr = df['length'].corr(df['skip_probability'])
    plt.text(0.05, 0.95, f'r = {corr:.3f}', 
             transform=plt.gca().transAxes, fontsize=12)
    
    plt.title('Word Length Effect on Skipping Probability')
    plt.xlabel('Word Length (characters)')
    plt.ylabel('Skipping Probability')
    plt.savefig(os.path.join(output_dir, 'length_skip_effect.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Word Frequency Effect on Skipping
    plt.figure()
    sns.scatterplot(data=df, x='log_frequency', y='skip_probability', 
                    size='total_occurrences', sizes=(20, 200),
                    alpha=0.3, legend='brief')
    sns.regplot(data=df, x='log_frequency', y='skip_probability', 
                scatter=False,
                line_kws={'linewidth': 2, 'color': 'red'},
                ci=95)
    
    # Add correlation coefficient
    corr = df['log_frequency'].corr(df['skip_probability'])
    plt.text(0.05, 0.95, f'r = {corr:.3f}', 
             transform=plt.gca().transAxes, fontsize=12)
    
    plt.title('Word Frequency Effect on Skipping Probability')
    plt.xlabel('Log Frequency (per million)')
    plt.ylabel('Skipping Probability')
    plt.savefig(os.path.join(output_dir, 'frequency_skip_effect.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Word Difficulty Effect on Regression
    plt.figure()
    sns.scatterplot(data=df, x='difficulty', y='regression_probability', 
                    size='total_occurrences', sizes=(20, 200),
                    alpha=0.3, legend='brief')
    sns.regplot(data=df, x='difficulty', y='regression_probability', 
                scatter=False,
                line_kws={'linewidth': 2, 'color': 'red'},
                ci=95)
    
    # Add correlation coefficient
    corr = df['difficulty'].corr(df['regression_probability'])
    plt.text(0.05, 0.95, f'r = {corr:.3f}', 
             transform=plt.gca().transAxes, fontsize=12)
    
    plt.title('Word Difficulty Effect on Regression Probability')
    plt.xlabel('Word Difficulty')
    plt.ylabel('Regression Probability')
    plt.savefig(os.path.join(output_dir, 'difficulty_regression_effect.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save detailed CSV files with more information
    
    # 1. Skipping analysis
    skip_analysis = df[[
        'word', 'original_forms', 'length', 'frequency', 'log_frequency', 
        'skip_probability', 'total_occurrences'
    ]].sort_values('skip_probability', ascending=False)
    skip_analysis.to_csv(os.path.join(output_dir, 'word_skipping_analysis.csv'), index=False)
    
    # 2. Regression analysis
    regression_analysis = df[[
        'word', 'original_forms', 'difficulty', 'regression_probability', 
        'total_occurrences'
    ]].sort_values('regression_probability', ascending=False)
    regression_analysis.to_csv(os.path.join(output_dir, 'word_regression_analysis.csv'), index=False)
    
    # 3. Full dataset
    df.to_csv(os.path.join(output_dir, 'complete_word_analysis.csv'), index=False)
    
    # Calculate summary statistics
    summary_stats = {
        'skipping': {
            'mean_probability': df['skip_probability'].mean(),
            'std_probability': df['skip_probability'].std(),
            'correlation_with_length': df['skip_probability'].corr(df['length']),
            'correlation_with_log_freq': df['skip_probability'].corr(df['log_frequency'])
        },
        'regression': {
            'mean_probability': df['regression_probability'].mean(),
            'std_probability': df['regression_probability'].std(),
            'correlation_with_difficulty': df['regression_probability'].corr(df['difficulty'])
        }
    }
    
    # Save summary statistics with more detail
    with open(os.path.join(output_dir, 'analysis_summary.txt'), 'w') as f:
        f.write("Word Skipping Analysis:\n")
        f.write(f"Total unique words analyzed: {len(df)}\n")
        f.write(f"Mean skip probability: {summary_stats['skipping']['mean_probability']:.3f}\n")
        f.write(f"Std skip probability: {summary_stats['skipping']['std_probability']:.3f}\n")
        f.write(f"Correlation with length: {summary_stats['skipping']['correlation_with_length']:.3f}\n")
        f.write(f"Correlation with log frequency: {summary_stats['skipping']['correlation_with_log_freq']:.3f}\n\n")
        
        f.write("Word Regression Analysis:\n")
        f.write(f"Mean regression probability: {summary_stats['regression']['mean_probability']:.3f}\n")
        f.write(f"Std regression probability: {summary_stats['regression']['std_probability']:.3f}\n")
        f.write(f"Correlation with difficulty: {summary_stats['regression']['correlation_with_difficulty']:.3f}\n")
        
        # Add distribution statistics
        f.write("\nDistribution Statistics:\n")
        f.write("Word Lengths: min={:.0f}, max={:.0f}, mean={:.1f}\n".format(
            df['length'].min(), df['length'].max(), df['length'].mean()))
        f.write("Log Frequencies: min={:.2f}, max={:.2f}, mean={:.2f}\n".format(
            df['log_frequency'].min(), df['log_frequency'].max(), df['log_frequency'].mean()))
        f.write("Difficulties: min={:.2f}, max={:.2f}, mean={:.2f}\n".format(
            df['difficulty'].min(), df['difficulty'].max(), df['difficulty'].mean()))
    
    return summary_stats

def main():
    # Set up directories
    output_dir = "/home/baiy4/ScanDL/scripts/data/zuco/bai_word_probability_analysis"
    plots_dir = os.path.join(output_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    # Collect word statistics
    print("Collecting word statistics...")
    df = collect_word_statistics()
    
    # Analyze and create plots
    print("Analyzing relationships and creating plots...")
    summary_stats = analyze_and_plot_relationships(df, plots_dir)
    
    # Print summary
    print("\nAnalysis complete!")
    print(f"Total unique words analyzed: {len(df)}")
    print(f"\nSkipping Statistics:")
    print(f"Mean skip probability: {summary_stats['skipping']['mean_probability']:.3f}")
    print(f"Correlation with length: {summary_stats['skipping']['correlation_with_length']:.3f}")
    print(f"Correlation with log frequency: {summary_stats['skipping']['correlation_with_log_freq']:.3f}")
    
    print(f"\nRegression Statistics:")
    print(f"Mean regression probability: {summary_stats['regression']['mean_probability']:.3f}")
    print(f"Correlation with difficulty: {summary_stats['regression']['correlation_with_difficulty']:.3f}")
    
    print(f"\nResults saved in: {output_dir}")

if __name__ == "__main__":
    main() 
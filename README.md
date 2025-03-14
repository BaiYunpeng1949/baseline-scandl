# ScanDL

![scandl-output](img/scanpath-exp-regular.png)

This repository contains the code to reproduce the experiments in [ScanDL: A Diffusion Model for Generating Synthetic Scanpaths on Texts](https://aclanthology.org/2023.emnlp-main.960/).

## Summary
* Our proposed model ScanDL is the first diffusion model for synthetic scanpath generation
* ScanDL is able to exhibit human-like reading behavior

![scandl-workflow](img/scandl-overview.png)

## Setup

### Clone this repository

```bash
git clone git@github.com:dili-lab/scandl
cd scandl
```


### Install requirements
The code is based on the PyTorch and huggingface modules.
```bash
pip install -r requirements.txt
```

### Download data

The CELER data can be downloaded from this [link](https://github.com/berzak/celer), where you need to follow the description.

The ZuCo data can be downloaded from this [OSF repository](https://osf.io/q3zws/). You can use `scripts/get_zuco_data.sh` to automatically download the ZuCo data. Note, ZuCo is a big dataset and requires a lot of storage.

Make sure you adapt the path to the folder that contains both the ```celer``` and the ```zuco``` in the file ```CONSTANTS.py```. If you use aboves bash script `scripts/get_zuco_data.sh`, the `zuco` paths is `data/`.
Make sure there are no whitespaces in the zuco directories (there might be when you download the data). You might want to check ```sp_load_celer_zuco.load_zuco()``` for the spelling of the directories.


### Preprocess data

Preprocessing the eye-tracking data takes time. It is thus recommended to perform the preprocessing once for each setting and save the preprocessed data in a directory ``processed_data``.
This not only saves time if training is performed several times but it also ensures the same data splits for each training run in the same setting.
For preprocessing and saving the data, run
```bash
python -m scripts.create_data_splits
```

## Training

Execute the following commands to perform the training.

### Notes
- To execute the [training commands](#training-commands), you need GPUs setup with [CUDA](https://developer.nvidia.com/cuda-toolkit).
- `--nproc_per_node` indicates the number of GPUs over which you want to split training.
- If you want to start multiple training processes at the same time, change `--master_port` to be different for all of them.
- `--load_train_data processed_data` means that the preprocessed data is loaded from the folder `processed_data`. If the data has not been preprocessed and saved, leave this argument away.

## Training Commands
To execute the training commands below, you need GPUs setup with [CUDA](https://developer.nvidia.com/cuda-toolkit).

#### New Reader setting
```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --master_port=12233 \
    --use_env scripts/sp_run_train.py \
    --corpus celer \
    --inference cv \
    --load_train_data processed_data \
    --num_transformer_heads 8 \
    --num_transformer_layers 12 \
    --hidden_dim 256 \
    --noise_schedule sqrt \
    --learning_steps 80000 \
    --log_interval 500 \
    --eval_interval 500 \
    --save_interval 5000 \
    --data_split_criterion reader
```

#### New Sentence setting
```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --master_port=12233 \
    --use_env scripts/sp_run_train.py \
    --corpus celer \
    --inference cv \
    --load_train_data processed_data \
    --num_transformer_heads 8 \
    --num_transformer_layers 12 \
    --hidden_dim 256 \
    --noise_schedule sqrt \
    --learning_steps 80000 \
    --log_interval 500 \
    --eval_interval 500 \
    --save_interval 5000 \
    --data_split_criterion sentence
```

#### New Reader/New Sentence setting
```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --master_port=12233 \
    --use_env scripts/sp_run_train.py \
    --corpus celer \
    --inference cv \
    --load_train_data processed_data \
    --num_transformer_heads 8 \
    --num_transformer_layers 12 \
     --hidden_dim 256 \
    --noise_schedule sqrt \
    --learning_steps 80000 \
    --log_interval 500 \
    --eval_interval 500 \
    --save_interval 5000 \
    --data_split_criterion combined
```

#### Cross-dataset setting
```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --master_port=12233 \
    --use_env scripts/sp_run_train.py \
    --corpus celer \
    --inference zuco \
    --load_train_data processed_data \
    --num_transformer_heads 8 \
    --num_transformer_layers 12 \
    --hidden_dim 256 \
    --noise_schedule sqrt \
    --learning_steps 80000 \
    --log_interval 500 \
    --eval_interval 500 \
    --save_interval 5000 \
    --notes cross_dataset \
    --data_split_criterion scanpath
```

#### Ablation: without positional embedding and BERT embedding (New Reader/New Sentence)
```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --master_port=12233 \
    --use_env scripts/sp_run_train_ablation.py \
    --corpus celer \
    --inference cv \
    --load_train_data processed_data \
    --num_transformer_heads 8 \
    --num_transformer_layers 12 \
    --hidden_dim 256 \
    --noise_schedule sqrt \
    --learning_steps 80000 \
    --log_interval 50 \
    --eval_interval 500 \
    --save_interval 5000 \
    --data_split_criterion combined \
    --notes ablation-no-pos-bert
```

#### Ablation: without condition (sentence): unconditional scanpath generation (New Reader/New Sentence)
```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --master_port=12233 \
    --use_env scripts/sp_run_train_ablation_no_condition.py \
    --corpus celer \
    --inference cv \
    --num_transformer_heads 8 \
    --num_transformer_layers 12 \
    --hidden_dim 256 \
    --noise_schedule sqrt \
    --learning_steps 80000 \
    --log_interval 50 \
    --eval_interval 500 \
    --save_interval 5000 \
    --data_split_criterion combined \
    --notes ablation-no-condition
```

#### Ablation: cosine noise schedule (New Reader/New Sentence)
```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --master_port=12233 \
    --use_env scripts/sp_run_train.py \
    --corpus celer \
    --inference cv \
    --load_train_data processed_data \
    --num_transformer_heads 8 \
    --num_transformer_layers 12 \
    --hidden_dim 256 \
    --noise_schedule cosine \
    --learning_steps 80000 \
    --log_interval 500 \
    --eval_interval 500 \
    --save_interval 5000 \
    --data_split_criterion combined
```

#### Ablation: linear noise schedule (New Reader/New Sentence)
```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --master_port=12233 \
    --use_env scripts/sp_run_train.py \
    --corpus celer \
    --inference cv \
    --load_train_data processed_data \
    --num_transformer_heads 8 \
    --num_transformer_layers 12 \
    --hidden_dim 256 \
    --noise_schedule linear \
    --learning_steps 80000 \
    --log_interval 500 \
    --eval_interval 500 \
    --save_interval 5000 \
    --data_split_criterion combined
```



## Inference

### NOTES
- ```checkpoint-path``` to indicte the folder name within the  directory that refers to your trained model
- ```--no_gpus``` indicates the number of GPUs across which you split the inference. It is recommended to set it to 1; if inference is split on multiple GPUs, each process will produce a separate output files which will have to be combined before evaluation can be run on them.
- ```--bsz``` is the batch size.
- ```--cv``` must be given for the cross-validation settings and it is not given for the cross-dataset setting.
- ```--load_test_data processed_data``` is given if the data has been preprocessed and split and saved already before training; otherwise leave it away. It is never given for the ablation case of unconditional scanpath generation.

If you run several inference processes at the same time, make sure to choose a different ```--seed``` for each of them. During training, the model is saved for many checkpoints. If you want to run inference on every checkpoint, leave the argument ```--run_only_on``` away. However, inference is quite costly time-wise and it is thus sensible to only
specify certain checkpoints onto which inference should be run. For that purpose, the exact path to that saved model must be given.

<br>

### Inference Commands

Adapt the following paths/variables:

- [MODEL_DIR]

- [FOLD_IDX]

- [STEPS]

<br>

For the settings:
* New Reader
* New Sentence
* New Reader/New Sentence
* Ablation: cosine noise schedule (New Reader/New Sentence)
* Ablation: linear noise schedule (New Reader/New Sentence)

```bash
python -u scripts/sp_run_decode.py \
    --model_dir checkpoint-path/[MODEL_DIR] \
    --seed 60 \
    --split test \
    --cv \
    --no_gpus 1 \
    --bsz 24 \
    --run_only_on 'checkpoint-path/[MODEL_DIR]/fold-[FOLD_IDX]/ema_0.9999_0[STEPS].pt' \
    --load_test_data processed_data
```

Cross-dataset:
```bash
python -u scripts/sp_run_decode.py \
    --model_dir checkpoint-path/[MODEL_DIR] \
    --seed 60 \
    --split test \
    --no_gpus 1 \
    --bsz 24 \
    --run_only_on 'checkpoint-path/[MODEL_DIR]/ema_0.9999_0[STEPS].pt' \
    --load_test_data processed_data
```

Ablation: without positional embedding and BERT embedding (New Reader/New Sentence)
```bash
python -u scripts/sp_run_decode_ablation.py \
    --model_dir checkpoint-path/[MODEL_DIR] \
    --seed 60 \
    --split test \
    --cv \
    --no_gpus 1 \
    --bsz 24 \
    --load_test_data processed_data \
    --run_only_on 'checkpoint-path/[MODEL_DIR/fold-[FOLD_IDX]/ema_0.9999_0[STEPS].pt'
```

Ablation: without condition (sentence): unconditional scanpath generation (New Reader/New Sentence)
```bash
python -u scripts/sp_run_decode_ablation_no_condition.py \
    --model_dir checkpoint-path/[MODEL_DIR] \
    --seed 60 \
    --split test \
    --cv \
    --no_gpus 1 \
    --bsz 24 \
    --run_only_on 'checkpoint-path/[MODEL_DIR]/fold-[FOLD_IDX]/ema_0.9999_0[STEPS].pt'
```


## Evaluation

To run the evaluation on the ScanDL output, again indicate the model dir in ```generation_outputs```:<br>

[MODEL_DIR]:

The argument ```--cv``` should be used for the evaluation on all cross-validation settings. <br>

For all cases except for the Cross-dataset:
```bash
python -m scripts.sp_eval --generation_outputs [MODEL_DIR] --cv
```

For the Cross-dataset setting:
```bash
python -m scripts.sp_eval --generation_outputs [MODEL_DIR]
```


## Psycholinguistic Analysis

To run the psycholinguistic analysis, first compute reading measures as well as psycholinguistic effects:<br>
Set ```MODEL_DIR``` to be the model directory in ```generation_outputs```.<br>

### NOTES
- ```--seed``` should be the same seed as used during inference.
- ```--setting``` to 'reader' for the New Reader setting, 'sentence' for the New Sentence setting, 'combined' for the 'New Reader/New Sentence setting', and 'cross_dataset' for cross dataset (train on celer, test on zuco).
- ```--steps``` to the number of training steps for the saved model checkpoint on which you have run the inference (e.g., 80000). 

```bash
python model_analyses/psycholinguistic_analysis.py --model [MODEL_DIR] --steps [N_STEPS] --setting [SETTING] --seed [SEED]
```

The reading measure files will be stored in the directory `pl_analysis/reading_measures`.

To fit the generalized linear models, run
```bash
Rscript --vanilla model_analyses/compute_effects.R --setting [SETTING] --steps [N_STEPS]
```

The fitted models will be saved as RDS-files in the directory `model_fits`.

To compare the effect sizes between the different models, run
```bash
Rscript --vanilla model_analyses/analyze_fit.R --setting [SETTING] --steps [N_STEPS]
```

## Citation

If you are using ScanDL, please consider citing our work:

```bibtex
@inproceedings{bolliger2023scandl,
    author = {Bolliger, Lena S. and Reich, David R. and Haller, Patrick and Jakobi, Deborah N. and Prasse, Paul and J{\"a}ger, Lena A.},
    title = {{S}can{DL}: {A} Diffusion Model for Generating Synthetic Scanpaths on Texts},
    booktitle={The 2023 Conference on Empirical Methods in Natural Language Processing},
    year={2023},
    publisher = {Association for Computational Linguistics},
}
```


<br>

## Acknowledgements

As indicated in the paper, our code is based on the [implementation](https://github.com/Shark-NLP/DiffuSeq) of [DiffuSeq](
https://doi.org/10.48550/arXiv.2210.08933).

# Data Processing Scripts

This directory contains scripts for processing and analyzing reading behavior data.

## Scripts Overview

### Data Processing Pipeline

1. `create_word_frequencies.py`: Processes SUBTLEX dataset to create word frequency information
   - Calculates frequency per million and log frequency
   - Handles data cleaning and validation
   - Output: `word_frequencies.json`

2. `create_word_predictabilities.py`: Calculates word predictability using NLTK language model
   - Uses Brown corpus for training a trigram model with Kneser-Ney smoothing
   - Calculates raw predictability scores (0-1)
   - Calculates logit predictability: 0.5 * ln(pred/(1-pred))
   - Handles edge cases:
     - For pred=0: uses 1/(2*83)
     - For pred=1: uses (2*83-1)/(2*83)
     - where 83 is the number of complete predictability protocols
   - Output: `word_predictabilities.json`

3. `analyze_reading_patterns.py`: Analyzes reading behavior for each participant
   - Processes fixation sequences
   - Identifies word skipping and regression patterns
   - Combines frequency, predictability, and eye-tracking metrics
   - Output: Individual JSON files per participant in `bai_reading_pattern_analysis/`

4. `analyze_word_probabilities.py`: Generates statistical analysis and visualizations
   - Calculates word-level statistics
   - Creates visualization plots for:
     - Word length effects
     - Frequency effects
     - Predictability effects
     - Logit predictability distribution and regression analysis
     - Predictability class analysis (5 classes based on logit values)
   - Output: Analysis files and plots in `bai_word_probability_analysis/`

## Output Files

### Word Features
- `word_frequencies.json`: Word frequency data from SUBTLEX
- `word_predictabilities.json`: Word predictability scores and logit transformations

### Analysis Results
- `complete_word_analysis.csv`: Full dataset with all metrics
- `word_skipping_analysis.csv`: Detailed skipping behavior analysis
- `word_regression_analysis.csv`: Detailed regression behavior analysis
- `analysis_summary.txt`: Statistical summary of all analyses

### Visualization Plots
- `length_skip_effect.png`: Word length effect on skipping
- `frequency_skip_effect.png`: Word frequency effect on skipping
- `predictability_skip_effect.png`: Word predictability effect on skipping
- `logit_predictability_distribution.png`: Logit predictability regression analysis
- `logit_predictability_histogram.png`: Distribution of logit predictability values
- `pred_class_skip_effect.png`: Skipping probability by predictability class
- `difficulty_regression_effect.png`: Word difficulty effect on regression

## Predictability Classes

Words are categorized into five logit-based predictability classes:
1. Class 1: -2.553 to -1.5
2. Class 2: -1.5 to -1.0
3. Class 3: -1.0 to -0.5
4. Class 4: -0.5 to 0
5. Class 5: 0 to 2.553

## Usage

1. Run scripts in order:
```bash
python create_word_frequencies.py
python create_word_predictabilities.py
python analyze_reading_patterns.py
python analyze_word_probabilities.py
```

2. Check output directories for results:
- `/scripts/data/` for JSON files
- `/scripts/data/zuco/bai_reading_pattern_analysis/` for per-participant analysis
- `/scripts/data/zuco/bai_word_probability_analysis/` for statistical analysis and plots

## Dependencies

- Python 3.6+
- numpy
- pandas
- matplotlib
- seaborn
- nltk
- tqdm




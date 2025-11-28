# Climate-War Discourse Analysis: Ukrainian Telegram Channels

## Overview
Analysis code for "Mechanistic early warnings of social tipping from discourse changepoints"

---

## 1. System Requirements

### Software Dependencies
- Python 3.9.6 or higher
- Operating Systems: Linux (Ubuntu 22.04+), macOS 13+, Windows 10/11
- All package dependencies listed in `requirements.txt`:
  - prophet==1.1.6
  - bertopic==0.16.4
  - statsmodels==0.14.4
  - scikit-learn==1.6.1
  - spacy==3.8.3
  - pandas==2.2.3
  - numpy==1.26.1
  - [see requirements.txt for complete list]

### Tested Versions
- Successfully tested on:
  - macOS 15.7 with Python 3.9.6

### Hardware Requirements
- Minimum: 8GB RAM, standard processor
- Recommended: 16GB RAM, multi-core processor

---

## 2. Installation Guide

### Installation Steps
```bash
# 1. Clone the repository
git clone https://github.com/tustyianovych/climate-posts-ukr-data.git
cd climate-posts-ukr-data

# 2. Create virtual environment
python3.9 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Upgrade pip, and install wheel and setuptools
pip3 install --upgrade pip setuptools wheel

# 4. Install dependencies
pip install -r requirements.txt

# # 5. Download spaCy Ukrainian language model
# python -m spacy download uk_core_news_trf
```

### Installation Time
- **Expected time:** 5-10 minutes on standard desktop computer with stable internet connection
- Depends on internet speed for downloading packages (~800MB total)

---

<!-- ## 3. Demo

### Demo Instructions

Run the demo notebook with sample data:
```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Launch Jupyter
jupyter notebook

# Open and run: notebooks/demo.ipynb
```

Or run from command line:
```bash
python scripts/run_demo.py
```

### Expected Output
The demo will:
1. Load sample dataset (100 posts)
2. Detect changepoints using Prophet (~3-5 changepoints expected)
3. Generate topic model (5-7 topics expected)
4. Create visualization outputs in `demo_output/` folder
5. Print summary statistics

### Expected Run Time
- **Demo runtime:** 2-3 minutes on standard desktop computer (Intel i5/AMD Ryzen 5 or equivalent, 16GB RAM)

### Demo Output Files
```
demo_output/
├── changepoints_plot.png
├── topic_distribution.png
├── tsne_visualization.png
└── summary_statistics.txt
```

--- -->

## 4. Instructions for Use

### Running with datasets in the data directory


#### Execution Steps
1. **Run analysis notebooks in order:**
```bash
jupyter-notebook
```

Execute notebooks in the respective `notebooks` folder sequentially:
- `01_data_exploration/eda.ipynb` - Clean and prepare data, compute reaction score, and train fastText and BERTopic models
- `02_changepoint_detection/prophet-model-log-transformed-percentage-change-mas.ipynb` - Train Prophet models on reaction score and detect changepoints 
- `03_text_analysis/bertopic-inference.ipynb` - Generate topics and embeddings with the BERTopic model trained in `01_data_exploration/eda.ipynb`
- `03_text_analysis/t-sne-text-data.ipynb` - Perform PCA and t-SNE dimensionality reduction, and visualize the results. 
- `04_named_entity_recognition/named-entity-recognition.ipynb` - Run named entity recognition.
- `05_causal_analysis/DAG-Hypothesis-Implementation.ipynb` - Structural equation modeling

3. **Outputs** will be saved in `results/` folder
<!-- 
#### Configuration
Edit `config.py` to adjust parameters:
- `CHANGEPOINT_PRIOR_SCALE`: Prophet sensitivity (default: 0.05)
- `N_TOPICS`: Number of topics (default: 15)
- `RANDOM_SEED`: For reproducibility (default: 42) -->

### Expected Runtime on Full Dataset
- Data preprocessing: ~10-15 minutes
- Prophet analysis: ~15-20 minutes
- Topic modeling: ~30-45 minutes
- Semantic analysis: ~10-15 minutes
- SEM analysis: ~5 minutes
- **Total: ~1.5-2 hours** (excluding data collection)

---

## 5. Reproduction Instructions

### Reproducing Paper Results

To reproduce all results from the manuscript:
<!-- 
1. **Obtain the full datasets** (see Data Availability section in paper)
   - Place in `data` folder.

2. **Run complete pipeline:**
```bash
python scripts/reproduce_paper_results.py
``` -->

Run notebooks manually in order (01-05 as above)

<!-- 3. **Verify outputs match manuscript:**
   - Table 1: `results/changepoint_summary.csv`
   - Table 2: `results/topic_distribution.csv`
   - Table 3: `results/sem_results.csv`
   - Figure 2: `results/figures/prophet_results.png`
   - Figure 3: `results/figures/tsne_clustering.png`
   - Figure 4: `results/figures/dag_structure.png` -->

<!-- 4. **Check reproducibility:**
```bash
python scripts/verify_reproducibility.py
```
This script compares your outputs with reference outputs and reports any discrepancies. -->

### Notes on Reproducibility
<!-- - Random seeds are fixed (seed=42) throughout -->
- Minor numerical variations (<1%) may occur due to:
  - Different hardware/OS
  - Library version differences
  - Floating-point precision
- Core findings (changepoint dates, topic assignments, SEM coefficients) should match exactly

<!-- ### Troubleshooting -->
<!-- See `TROUBLESHOOTING.md` for common issues and solutions. -->

---

<!-- ## Citation
```bibtex
[Your citation here]
``` -->

## License
MIT License - See LICENSE file

## Contact
Taras.O.Ustyianovych@lpnu.ua
<!-- ```

<!-- ### 3. **Create Demo Notebook** (`notebooks/demo.ipynb`) -->

Simple notebook that runs on demo data and completes in 2-3 minutes.

### 4. **Create Reproduction Script** (optional but recommended)

`scripts/reproduce_paper_results.py` - automated script to regenerate all paper results.

--- -->

## Summary Checklist

**In your repository, you need:**

- ☑ `README.md` (with all 4 required sections + reproduction)
- ☑ `requirements.txt` (already have)
- ☑ `LICENSE` (MIT recommended)
- ☑ `data/` (raw and processed datasets with backups)
- ☑ `notebooks/01-05_*.ipynb` (your analysis notebooks)
<!-- - ☑ `config.py` (configuration parameters) -->
<!-- - ☑ `scripts/reproduce_paper_results.py` (optional but recommended) -->
- ☑ Clear folder structure

**Folder structure:**
```
climate-posts-ukr-data/
├── README.md
├── requirements.txt
├── LICENSE
└── results/
│   └── external_data/
│   └── processed/
│   └── prophet_data/
│   └── raw/
└── models/
    └── bertopic-models/
    └── fasttext-models/
<!-- ├── config.py -->
├── notebooks/
│   ├── 01_data_exploration/
│   ├── 02_changepoint_detection
│   ├── 03_text_analysis
│   ├── 04_named_entity_recognition
│   └── 05_causal_analysis
└── results/
    └── (generated outputs)
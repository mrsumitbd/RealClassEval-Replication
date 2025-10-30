# 📑 Replication Package for [RealClassEval]

This repository contains the replication package for the paper:  
**[Beyond Synthetic Benchmarks: Evaluating LLM Performance on Real-World Class-Level Code Generation]**  
Authors: [Musfiqur Rahman, SayedHassan Khatoonabadi, Emad Shihab]  
Published at: [Conference/Journal, Year]  

The goal of this repository is to ensure reproducibility of all experiments, figures, and results presented in the paper.

---
## Clone the repository
```bash
git clone https://github.com/mrsumitbd/RealClassEval-Replication.git
cd RealClassEval-Replication
```
---

## 📂 Repository Structure
```text
RealClassEval-Replication/
├── notebooks/         # Jupyter notebooks for experiments, analysis, figures
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_training.ipynb
│   └── 03_results.ipynb
│
├── src/               # Python source code (modules, utilities, pipelines)
│   ├── __init__.py
│   ├── data_loader.py
│   ├── model.py
│   └── utils.py
│
├── data/              # Placeholder for datasets (not stored in repo)
│   └── README.md
│
├── results/           # Output results (figures, logs, metrics, tables)
│   └── README.md
│
├── setup.sh           # Setup script for Linux/macOS
├── .gitignore         # Ignore unnecessary files
├── .env.example       # Template for environment variables
├── requirements.txt   # Python dependencies
├── environment.yml    # Conda environment file
├── README.md          # Documentation
└── LICENSE            # License file
```
---

## ⚙️ Setup Instructions (Linux/macOS)

### Option 1: Quick setup (recommended)
```bash
bash setup.sh
```
This will:
- Verify that Python 3.11 is installed
- Create a virtual environment in venv/
- Install all dependencies from requirements.txt

After running the script, activate the environment manually:
```bash
source venv/bin/activate
```

### Option 2: Manual setup
#### 1. Create a virtual environment (Python 3.11)
```bash
python3.11 -m venv venv
source venv/bin/activate   # On macOS/Linux
```

#### 2. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```


### Option 3: Using Conda
If you prefer Conda, use the provided `environment.yml`:

```bash
# Create the environment
conda env create -f environment.yml

# Activate it
conda activate OpenClassGen-replication
```

After setting up the environment (using one of the three options above), create a `.env` file in the root directory by copying the `.env.example`:
```bash
cp .env.example .env   # Linux/macOS
```
---

## 🛠️ System Dependencies

In addition to the Python environment, some scripts require external tools.

### `cloc` (Count Lines of Code)

This project uses [`cloc`](https://github.com/AlDanial/cloc) to count lines of code.  
You need to install it separately on your system.

#### macOS
If you use Homebrew:
```bash
brew install cloc
```

#### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install cloc
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install cloc
```
Once installed, you can verify with:
```bash
cloc --version
```
---

## 📊 Datasets

Datasets are not included in this repository due to size and licensing restrictions.
Please follow the instructions in data/README.md to download and prepare the required datasets.

---

## 📈 Results

All results (figures, logs, tables) will be stored in the results/ directory.
Pre-generated results are provided for reference where possible.

## 📜 License

This project is licensed under the MIT License.

## 🙏 Citation

If you use this replication package, please cite our paper:
```bib
@inproceedings{yourbibkey,
  author    = {Your Name and Co-authors},
  title     = {Paper Title},
  booktitle = {Conference/Journal},
  year      = {2025}
}
```

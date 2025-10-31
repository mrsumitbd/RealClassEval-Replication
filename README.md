# 📑 Replication Package for RealClassEval

This repository contains the replication package for the paper:  
**[Beyond Synthetic Benchmarks: Evaluating LLM Performance on Real-World Class-Level Code Generation](https://arxiv.org/abs/2510.26130)**
Authors: [Musfiqur Rahman](https://das.encs.concordia.ca/members/musfiqur-rahman), [SayedHassan Khatoonabadi](https://das.encs.concordia.ca/members/hassan-khatoonabadi), [Emad Shihab](https://das.encs.concordia.ca/members/emad-shihab)
Published at: arXiv.org, 2025  

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
│   └── plot_generator.ipynb
│
├── src/               # Python source code (modules, utilities, pipelines)
│   ├── __init__.py
│   ├── rag/
│   ├── ...
│   └── utils.py
│
├── data/              # Placeholder for datasets and metadata
│   ├── functional_correctness_data/
│   └── generated_code/
│
├── results/           # Output results (figures, metrics, etc.)
│   ├── rq1/
│   ├── ...
│   └── rq4/
│
├── rag_experiments/ # Stores all files generated during running rag
│
├── functional_correctness_test_folder/ # This is where the functional correctness test happened. Kept is separate for easier access and organization
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

Datasets are included in the `data/` folder.

---

## 📈 Results

All results (figures, tables) are stored in the `results/` directory.
Pre-generated results are provided for reference where possible.

## 📜 License

This project is licensed under the MIT License.

## 🙏 Citation

If you use this replication package, please cite our paper:
```bib
@misc{rahman2025syntheticbenchmarksevaluatingllm,
      title={Beyond Synthetic Benchmarks: Evaluating LLM Performance on Real-World Class-Level Code Generation}, 
      author={Musfiqur Rahman and SayedHassan Khatoonabadi and Emad Shihab},
      year={2025},
      eprint={2510.26130},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2510.26130}, 
}
```

# Cultural Encoding in Large Language Models: Dataset & Analysis Scripts

[![arXiv](https://img.shields.io/badge/arXiv-2024.xxxxx-b31b1b.svg)](https://arxiv.org/abs/xxxx.xxxxx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Research Finding**: Chinese LLMs exhibit 30.6 percentage points higher brand mention rates than International LLMs (88.9% vs. 58.3%, χ²=226.60, p<.001), even in pure-English queries. This disparity reveals systematic cultural encoding in AI training data.

---

## 📊 About This Repository

This repository contains the dataset and analysis scripts for the paper:

**"Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery"**

*Huang, J., Situ, R., & Ye, R. (2024)*

### Repository Contents

- **Sample Dataset**: 100 query-LLM pairs demonstrating data structure
- **Analysis Scripts**: Complete statistical analysis and visualization code
- **Documentation**: Replication instructions and methodology details

---

## 🎓 Research Abstract

This study investigates **Cultural Encoding in Large Language Models**—systematic differences in brand recommendations arising from the linguistic and cultural composition of training data.

**Key Findings:**
- Chinese LLMs: 88.9% brand mention rate
- International LLMs: 58.3% brand mention rate
- Difference: 30.6 percentage points (χ²=226.60, p<.001, φ=0.34)

**Case Study**: Zhizibianjie (智子边界), a collaboration platform, demonstrates extreme cultural encoding:
- Chinese LLMs: 65.6% mention rate
- International LLMs: 0% mention rate
- Statistical significance: χ²=21.33, p<.001, φ=0.58

**Theoretical Contributions:**
1. **Cultural Encoding Framework**: Training data geography creates systematic brand visibility differences
2. **Existence Gap Concept**: Brands absent from training data lack "existence" in AI responses
3. **Data Moat Framework**: AI-visible content as a VRIN strategic resource

---

## 📦 Dataset

### Sample Dataset (This Repository)

**File**: `data_sample_100.json`

Contains 100 query-LLM pairs demonstrating:
- 6 LLMs tested (GPT-4o, Claude, Gemini, Qwen3, DeepSeek, Doubao)
- Multiple brands across different origins
- 10 query types covering diverse user intents
- Mention rates and sentiment analysis

### Complete Dataset (1,909 Queries)

The full dataset includes:
- 1,909 pure-English query-LLM pairs
- 30 brands (Western, Chinese, Global/Mixed)
- 10 query types with complete coverage
- Statistical analysis raw data
- Language validation process documentation

**📧 Data Access for Academic Research**

The complete dataset is available for academic research purposes. To request access:

1. **Email**: huangjunyao@zhizibianjie.com
2. **Subject**: "Request for GEO Dataset Access"
3. **Include**:
   - Your name and institution
   - Research purpose and methodology
   - Intended use of the dataset
   - Expected publication timeline

> **Note**: Due to API terms of service and privacy considerations, we provide the complete dataset through a review process to ensure academic use. We typically respond within 3-5 business days.

---

## 🚀 Analysis Scripts

This repository includes all analysis code used in the paper:

```
scripts/
├── validate_query_language.py    # Language validation (2,800→1,909 queries)
├── statistical_tests.py           # Chi-square, t-test, logistic regression
├── generate_tables.py             # Generate paper tables
├── analyze_cultural_bias.py       # Cultural encoding analysis
├── create_english_subset.py       # Create pure-English subset
├── test_zhizibianjie.py          # Case study analysis
├── analyze_chinese_brands.py      # Chinese brand analysis
└── generate_figures.py            # Visualization generation
```

### Running the Analysis

```bash
# Install dependencies
pip install -r requirements.txt

# Run statistical tests
python scripts/statistical_tests.py

# Generate tables
python scripts/generate_tables.py

# Generate figures
python scripts/generate_figures.py
```

---

## 📄 Citation

If you use this dataset or code in your research, please cite:

```bibtex
@article{huang2024cultural,
  title={Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery},
  author={Huang, Junyao and Situ, Ruimin and Ye, Renqin},
  journal={arXiv preprint arXiv:xxxx.xxxxx},
  year={2024},
  institution={OmniEdge (Zhizibianjie) AI Consulting Co., Ltd.}
}
```

---

## 👥 About the Authors

This research is conducted by the **AI Research Team at OmniEdge (Zhizibianjie)**, specializing in:
- Generative Engine Optimization (GEO)
- AI-mediated information discovery
- Cross-cultural LLM behavior analysis
- Brand visibility in AI systems

**Research Team:**
- **Junyao Huang** (Corresponding Author) - huangjunyao@zhizibianjie.com
- **Ruimin Situ** - situruimin@zhizibianjie.com
- **Renqin Ye** - yerenqin@zhizibianjie.com

**Institution**: OmniEdge (Zhizibianjie) AI Consulting Co., Ltd., Shenzhen, China

**Research Website**: [zhizibianjie.com](https://zhizibianjie.com)

---

## 🤝 Research Collaboration

We welcome academic collaborations on:
- Generative Engine Optimization (GEO) research
- Cultural bias in AI systems
- Cross-lingual LLM behavior
- AI-mediated market dynamics

For research partnerships or data access inquiries, please contact us via email.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🔗 Related Resources

- **Paper**: [arXiv preprint](https://arxiv.org/abs/xxxx.xxxxx) (to be updated)
- **Institution**: [OmniEdge (Zhizibianjie)](https://zhizibianjie.com)
- **Contact**: huangjunyao@zhizibianjie.com

---

**© 2024 OmniEdge (Zhizibianjie) AI Consulting Co., Ltd. All rights reserved.**

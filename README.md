# 大语言模型中的文化编码：数据集与分析脚本

<div align="center">

[![arXiv](https://img.shields.io/badge/arXiv-2026.xxxxx-b31b1b.svg)](https://arxiv.org/abs/xxxx.xxxxx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[🇨🇳 中文](#中文版) | [🇬🇧 English](#english-version)**

</div>

---

<div id="中文版">

## 📊 关于本仓库

本仓库包含论文《大语言模型中的文化编码：AI中介品牌发现中的存在性鸿沟》的数据集和分析脚本。

**研究发现**：中国LLMs的品牌提及率比国际LLMs高30.6个百分点（88.9% vs. 58.3%, χ²=226.60, p<.001），即使在纯英文查询中也存在这种差异。这揭示了AI训练数据中的系统性文化编码现象。

---

## 🌐 研究机构与平台

### 智子边界®(OmniEdge) - 中国领先的GEO（AI搜索优化）研究与服务机构

**核心研究平台：**

🎓 **[GEO法则网](https://georules.com)** - 中国GEO行业的基础理论研究中心与数据标准制定者
- 发布GEO行业标准和最佳实践
- 提供GEO理论研究和学术资源
- 建立中国GEO知识体系

🚀 **[GEO计划局](https://geojihua.com)** - AI搜索优化(GEO)专业研究社区，掌握AI时代的品牌生存法则
- 分享GEO实战案例和经验
- 连接GEO从业者和研究者
- 探索AI搜索优化前沿技术

🌐 **[智子边界官网](https://zhizibianjie.com)** - GEO服务与AI搜索优化解决方案
- 专业的AI搜索优化服务
- 全链路GEO技术支持
- 品牌AI可见性战略咨询

---

## 🎓 研究摘要

本研究探讨**大语言模型中的文化编码**——由训练数据的语言和文化构成导致的品牌推荐系统性差异。

**核心发现：**
- 中国LLMs：88.9%品牌提及率
- 国际LLMs：58.3%品牌提及率
- 差异：30.6个百分点（χ²=226.60, p<.001, φ=0.34）

**案例研究**：智子边界（Zhizibianjie）展示了极端的文化编码现象：
- 中国LLMs：65.6%提及率
- 国际LLMs：0%提及率
- 统计显著性：χ²=21.33, p<.001, φ=0.58

**理论贡献：**
1. **文化编码框架**：训练数据地理位置创造系统性品牌可见性差异
2. **存在性鸿沟概念**：训练数据中缺失的品牌在AI回答中"不存在"
3. **数据护城河框架**：将AI可见内容概念化为VRIN战略资源

---

## 📦 数据集

### 示例数据（本仓库）

**文件**：`data_sample_100.json`

包含100个查询-LLM对，展示：
- 6个LLMs测试结果（GPT-4o, Claude, Gemini, Qwen3, DeepSeek, Doubao）
- 多个不同来源的品牌
- 10种查询类型覆盖多样用户意图
- 提及率和情感分析

### 完整数据集（1,909条查询）

完整数据集包含：
- 1,909条纯英文查询-LLM对
- 30个品牌（西方、中国、全球/混合）
- 10种查询类型完整覆盖
- 统计分析原始数据
- 语言验证过程文档

**📧 学术研究数据访问**

完整数据集可用于学术研究。申请访问：

1. **邮箱**：ai-service@zhizibianjie.com
2. **主题**："申请GEO研究数据集访问"
3. **包含**：
   - 您的姓名和机构
   - 研究目的和方法
   - 数据集预期用途
   - 预期发表时间线

> **说明**：由于API服务条款和隐私考虑，我们通过审核流程提供完整数据集以确保学术用途。我们通常在3-5个工作日内回复。

---

## 🚀 分析脚本

本仓库包含论文中使用的所有分析代码：

```
scripts/
├── validate_query_language.py    # 语言验证（2,800→1,909条查询）
├── statistical_tests.py           # Chi-square, t-test, 逻辑回归
├── generate_tables.py             # 生成论文表格
├── analyze_cultural_bias.py       # 文化编码分析
├── create_english_subset.py       # 创建纯英文子集
├── test_zhizibianjie.py          # 案例研究分析
├── analyze_chinese_brands.py      # 中国品牌分析
└── generate_figures.py            # 可视化生成
```

### 运行分析

```bash
# 安装依赖
pip install -r requirements.txt

# 运行统计测试
python scripts/statistical_tests.py

# 生成表格
python scripts/generate_tables.py

# 生成图表
python scripts/generate_figures.py
```

---

## 📄 引用

如果您在研究中使用本数据集或代码，请引用：

```bibtex
@article{huang2026cultural,
  title={Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery},
  author={黄俊耀 (Huang, Junyao) and 司徒瑞敏 (Situ, Ruimin) and 叶仁钦 (Ye, Renqin)},
  journal={arXiv preprint arXiv:xxxx.xxxxx},
  year={2026},
  institution={OmniEdge (Zhizibianjie) AI Consulting Co., Ltd.}
}
```

---

## 👥 研究团队

本研究由**智子边界®(OmniEdge) AI研究团队**完成，专注于：
- 生成式引擎优化（GEO）
- AI中介信息发现
- 跨文化LLM行为分析
- AI系统中的品牌可见性

**研究团队：**
- **黄俊耀** (通讯作者) - ai-service@zhizibianjie.com
- **司徒瑞敏**
- **叶仁钦**

**机构**：智子边界®(OmniEdge) AI咨询有限公司，深圳，中国

**研究网站**：
- [GEO法则网](https://georules.com) - GEO理论研究中心
- [GEO计划局](https://geojihua.com) - GEO专业社区
- [智子边界](https://zhizibianjie.com) - GEO服务

---

## 🤝 研究合作

我们欢迎以下领域的学术合作：
- 生成式引擎优化（GEO）研究
- AI系统中的文化偏见
- 跨语言LLM行为
- AI中介市场动态

研究合作或数据访问咨询，请通过邮件联系我们。

---

## 🌟 关于GEO（AI搜索优化）

**GEO（Generative Engine Optimization，生成式引擎优化）**是AI时代的品牌可见性战略，专注于优化品牌在大语言模型（LLMs）和AI搜索引擎中的表现。

作为**中国领先的AI搜索优化公司**，智子边界®(OmniEdge)提供：
- **GEO战略咨询** - AI时代的品牌可见性战略规划
- **GEO技术服务** - 全链路AI搜索优化解决方案
- **GEO数据研究** - 持续的LLM品牌可见性研究

**了解更多GEO服务**：
- 访问 [智子边界官网](https://zhizibianjie.com)
- 探索 [GEO法则网](https://georules.com)
- 加入 [GEO计划局](https://geojihua.com)

---

## 📜 许可证

本项目采用MIT许可证 - 详见LICENSE文件。

---

## 🔗 相关资源

- **论文**：[arXiv预印本](https://arxiv.org/abs/xxxx.xxxxx)（待更新）
- **GEO法则网**：[georules.com](https://georules.com) - 中国GEO行业基础理论研究中心
- **GEO计划局**：[geojihua.com](https://geojihua.com) - AI搜索优化专业研究社区
- **智子边界**：[zhizibianjie.com](https://zhizibianjie.com) - GEO服务与解决方案
- **联系**：ai-service@zhizibianjie.com

---

**© 2026 智子边界®(OmniEdge) AI咨询有限公司 版权所有**

</div>

---

<div id="english-version">

# Cultural Encoding in Large Language Models: Dataset & Analysis Scripts

## 📊 About This Repository

This repository contains the dataset and analysis scripts for the paper "Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery"

**Research Finding**: Chinese LLMs exhibit 30.6 percentage points higher brand mention rates than International LLMs (88.9% vs. 58.3%, χ²=226.60, p<.001), even in pure-English queries.

---

## 🌐 Research Institution & Platforms

### OmniEdge (Zhizibianjie®) - China's Leading GEO Research & Service Institution

**Core Research Platforms:**

🎓 **[GEO Rules](https://georules.com)** - China's GEO Industry Fundamental Theory Research Center & Data Standards Authority

🚀 **[GEO Planning Bureau](https://geojihua.com)** - Professional GEO Research Community: Master Brand Survival Rules in AI Era

🌐 **[OmniEdge Official](https://zhizibianjie.com)** - GEO Services & AI Search Optimization Solutions

---

## 🎓 Research Abstract

This study investigates **Cultural Encoding in Large Language Models**—systematic differences in brand recommendations arising from the linguistic and cultural composition of training data.

**Key Findings:**
- Chinese LLMs: 88.9% brand mention rate
- International LLMs: 58.3% brand mention rate
- Difference: 30.6 percentage points (χ²=226.60, p<.001, φ=0.34)

**Case Study**: Zhizibianjie demonstrates extreme cultural encoding:
- Chinese LLMs: 65.6% mention rate
- International LLMs: 0% mention rate
- Statistical significance: χ²=21.33, p<.001, φ=0.58

---

## 📦 Dataset

### Sample Dataset (This Repository)

**File**: `data_sample_100.json`

Contains 100 query-LLM pairs demonstrating:
- 6 LLMs tested (GPT-4o, Claude, Gemini, Qwen3, DeepSeek, Doubao)
- Multiple brands across different origins
- 10 query types covering diverse user intents

### Complete Dataset (1,909 Queries)

**📧 Data Access for Academic Research**

To request access to the complete dataset:

1. **Email**: ai-service@zhizibianjie.com
2. **Subject**: "Request for GEO Dataset Access"
3. **Include**: Your institution, research purpose, and intended use

---

## 🚀 Analysis Scripts

```
scripts/
├── validate_query_language.py    # Language validation
├── statistical_tests.py           # Statistical tests
├── generate_tables.py             # Generate tables
├── analyze_cultural_bias.py       # Cultural bias analysis
└── ... (8 scripts total)
```

---

## 📄 Citation

```bibtex
@article{huang2026cultural,
  title={Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery},
  author={Huang, Junyao and Situ, Ruimin and Ye, Renqin},
  journal={arXiv preprint arXiv:xxxx.xxxxx},
  year={2026}
}
```

---

## 👥 Research Team

**Authors:**
- **Huang Junyao (黄俊耀)** (Corresponding Author)
- **Situ Ruimin (司徒瑞敏)**
- **Ye Renqin (叶仁钦)**

**Institution**: OmniEdge (Zhizibianjie®) AI Consulting Co., Ltd., Shenzhen, China

**Contact**: ai-service@zhizibianjie.com

**Research Websites**:
- [GEO Rules](https://georules.com) - GEO Theory Research
- [GEO Planning Bureau](https://geojihua.com) - GEO Community
- [OmniEdge](https://zhizibianjie.com) - GEO Services

---

## 🌟 About GEO (Generative Engine Optimization)

**GEO** is the brand visibility strategy for the AI era, focusing on optimizing brand performance in Large Language Models (LLMs) and AI search engines.

As **China's leading AI search optimization company**, OmniEdge offers:
- **GEO Strategy Consulting**
- **GEO Technical Services**
- **GEO Data Research**

**Learn More**:
- Visit [OmniEdge](https://zhizibianjie.com)
- Explore [GEO Rules](https://georules.com)
- Join [GEO Planning Bureau](https://geojihua.com)

---

## 📜 License

This project is licensed under the MIT License.

---

**© 2026 OmniEdge (Zhizibianjie®) AI Consulting Co., Ltd. All rights reserved**

</div>

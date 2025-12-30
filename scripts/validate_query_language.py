#!/usr/bin/env python3
"""
阶段1.1：查询语言验证
检查所有6个LLM是否使用相同语言查询

Author: GEO Research Team
Date: 2025-12-30
"""

import json
import random
from collections import defaultdict, Counter
import string
from typing import Dict, List


def detect_language(text: str) -> str:
    """
    简单检测文本语言

    Returns:
        'English', 'Chinese', or 'Mixed'
    """
    # 移除空格和标点
    cleaned = text.strip().translate(str.maketrans('', '', string.punctuation))

    if not cleaned:
        return 'Empty'

    # 检测中文字符
    chinese_chars = sum(1 for c in cleaned if '\u4e00' <= c <= '\u9fff')
    total_chars = len(cleaned)

    chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0

    if chinese_ratio > 0.3:
        return 'Chinese'
    elif chinese_ratio > 0:
        return 'Mixed'
    else:
        return 'English'


def analyze_queries(data_file: str, sample_size: int = 100) -> Dict:
    """分析查询语言分布"""

    print(f"加载数据文件: {data_file}")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"总记录数: {len(data)}")

    # 随机抽样
    if len(data) > sample_size:
        sample = random.sample(data, sample_size)
        print(f"随机抽样: {sample_size}条记录")
    else:
        sample = data
        print(f"使用全部数据: {len(data)}条记录")

    # 按LLM分组分析
    llm_queries = defaultdict(list)

    for record in sample:
        llm = record['llm']
        query = record['actual_query']
        llm_queries[llm].append(query)

    # 统计每个LLM的查询语言
    llm_language_stats = {}

    for llm, queries in llm_queries.items():
        language_counts = Counter()

        for query in queries:
            lang = detect_language(query)
            language_counts[lang] += 1

        total = len(queries)
        llm_language_stats[llm] = {
            'total': total,
            'languages': dict(language_counts),
            'english_pct': language_counts.get('English', 0) / total * 100,
            'chinese_pct': language_counts.get('Chinese', 0) / total * 100,
            'mixed_pct': language_counts.get('Mixed', 0) / total * 100
        }

    # 检查是否有样本查询
    sample_queries_by_llm = {}
    for llm in llm_queries.keys():
        sample_queries_by_llm[llm] = random.sample(llm_queries[llm],
                                                   min(5, len(llm_queries[llm])))

    return {
        'llm_language_stats': llm_language_stats,
        'sample_queries': sample_queries_by_llm,
        'total_records': len(data)
    }


def generate_report(analysis: Dict) -> str:
    """生成验证报告"""

    report_lines = []
    report_lines.append("="*70)
    report_lines.append("查询语言验证报告")
    report_lines.append("="*70)
    report_lines.append("")
    report_lines.append(f"数据来源: {analysis['total_records']}条记录")
    report_lines.append(f"分析方法: 随机抽样检测")
    report_lines.append("")
    report_lines.append("-"*70)
    report_lines.append("1. 各LLM查询语言统计")
    report_lines.append("-"*70)
    report_lines.append("")

    llm_stats = analysis['llm_language_stats']

    # 按英文占比排序
    sorted_llms = sorted(llm_stats.items(),
                        key=lambda x: x[1]['english_pct'],
                        reverse=True)

    for llm, stats in sorted_llms:
        report_lines.append(f"\n{llm}:")
        report_lines.append(f"  总查询数: {stats['total']}")
        report_lines.append(f"  语言分布:")
        for lang, count in stats['languages'].items():
            pct = count / stats['total'] * 100
            report_lines.append(f"    {lang}: {count} ({pct:.1f}%)")

    report_lines.append("")
    report_lines.append("-"*70)
    report_lines.append("2. 结论")
    report_lines.append("-"*70)
    report_lines.append("")

    # 检查是否所有LLM都用英文
    all_english = all(stats['english_pct'] > 95
                     for stats in llm_stats.values())

    all_chinese = all(stats['chinese_pct'] > 95
                      for stats in llm_stats.values())

    mixed = not (all_english or all_chinese)

    if all_english:
        report_lines.append("✅ 结论: 所有LLM都使用英文查询")
        report_lines.append("")
        report_lines.append("研究有效性: 可以安全地将差异归因于LLM文化背景，")
        report_lines.append("而非查询语言混淆。")
    elif all_chinese:
        report_lines.append("⚠️  结论: 所有LLM都使用中文查询")
        report_lines.append("")
        report_lines.append("研究有效性: 仍可比较LLM差异，但需要说明")
        report_lines.append("这是中文查询环境下的差异。")
    else:
        report_lines.append("❌ 结论: LLM使用混合语言查询")
        report_lines.append("")
        report_lines.append("研究有效性警告: 存在语言混淆变量！")
        report_lines.append("建议:")
        report_lines.append("  1. 分别分析英文和中文子集")
        report_lines.append("  2. 或者重新采集数据，统一查询语言")
        report_lines.append("  3. 或者调整研究问题为'语言×LLM交互效应'")

    report_lines.append("")
    report_lines.append("-"*70)
    report_lines.append("3. 样本查询示例")
    report_lines.append("-"*70)
    report_lines.append("")

    sample_queries = analysis['sample_queries']

    for llm, queries in sorted(sample_queries.items()):
        report_lines.append(f"\n{llm}:")
        for i, query in enumerate(queries, 1):
            lang = detect_language(query)
            report_lines.append(f"  [{i}] [{lang}] {query}")

    report_lines.append("")
    report_lines.append("="*70)
    report_lines.append("报告生成完毕")
    report_lines.append("="*70)

    return "\n".join(report_lines)


def main():
    """主函数"""
    data_file = '/Users/hjy/Project/arxiv_geo_001/tmp/task2/data/raw/geo_data_final_20251230_042232.json'

    print("开始查询语言验证...")
    analysis = analyze_queries(data_file, sample_size=100)

    print("\n生成验证报告...")
    report = generate_report(analysis)

    # 打印报告
    print("\n" + report)

    # 保存报告
    output_file = '/Users/hjy/Project/arxiv_geo_001/paper/paper1_cultural_bias/analysis_results/阶段1-1_查询语言验证报告.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✓ 报告已保存至: {output_file}")

    # 返回关键结论
    llm_stats = analysis['llm_language_stats']
    all_english = all(stats['english_pct'] > 95 for stats in llm_stats.values())

    return all_english


if __name__ == '__main__':
    main()

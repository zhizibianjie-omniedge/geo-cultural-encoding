#!/usr/bin/env python3
"""
创建纯英文查询子集并快速分析LLM文化编码效应

Author: GEO Research Team
Date: 2025-12-30
"""

import json
from collections import defaultdict
import numpy as np
from scipy import stats


def is_english_query(text: str) -> bool:
    """判断查询是否为纯英文"""
    # 不包含中文字符
    return not any('\u4e00' <= c <= '\u9fff' for c in text)


def create_english_subset(data_file: str, output_file: str):
    """创建纯英文查询子集"""

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 过滤纯英文查询
    english_only = [r for r in data if is_english_query(r['actual_query'])]

    print(f"原始数据: {len(data)}条")
    print(f"纯英文查询: {len(english_only)}条 ({len(english_only)/len(data)*100:.1f}%)")

    # 保存子集
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(english_only, f, ensure_ascii=False, indent=2)

    print(f"✓ 纯英文子集已保存至: {output_file}")

    return english_only


def quick_cultural_bias_analysis(data: list):
    """快速分析LLM文化编码效应"""

    print("\n" + "="*70)
    print("纯英文子集：LLM文化编码效应快速分析")
    print("="*70)

    # 按LLM分组
    llm_regions = {
        'GPT-4o Search Preview': 'International',
        'Claude Sonnet 4.5': 'International',
        'Gemini Pro Latest': 'International',
        'Qwen3 Max Preview': 'Chinese',
        'DeepSeek V3.2 Exp': 'Chinese',
        'Doubao 1.5 Thinking Pro': 'Chinese'
    }

    llm_stats = defaultdict(lambda: {
        'total': 0,
        'mentioned': 0,
        'sentiments': []
    })

    for record in data:
        llm = record['llm']
        mentioned = record['response']['mention']
        sentiment = record['response']['sentiment']

        llm_stats[llm]['total'] += 1
        if mentioned:
            llm_stats[llm]['mentioned'] += 1

        # 情感编码
        sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
        llm_stats[llm]['sentiments'].append(sentiment_map.get(sentiment, 0))

    # 计算统计
    print("\n1. 品牌提及率分析")
    print("-"*70)

    results = []
    for llm, stats in llm_stats.items():
        region = llm_regions.get(llm, 'Unknown')
        mention_rate = stats['mentioned'] / stats['total'] * 100
        avg_sentiment = np.mean(stats['sentiments'])

        results.append({
            'LLM': llm,
            'Region': region,
            'Mention_Rate': mention_rate,
            'Total': stats['total'],
            'Avg_Sentiment': avg_sentiment
        })

    # 按地区汇总
    intl_stats = [r for r in results if r['Region'] == 'International']
    china_stats = [r for r in results if r['Region'] == 'Chinese']

    intl_mention = np.mean([r['Mention_Rate'] for r in intl_stats])
    china_mention = np.mean([r['Mention_Rate'] for r in china_stats])

    intl_sentiment = np.mean([r['Avg_Sentiment'] for r in intl_stats])
    china_sentiment = np.mean([r['Avg_Sentiment'] for r in china_stats])

    print(f"\n国际LLM平均提及率: {intl_mention:.1f}%")
    print(f"中国LLM平均提及率: {china_mention:.1f}%")
    print(f"差异: {china_mention - intl_mention:+.1f}个百分点")

    # Chi-square检验
    intl_mentioned = sum(1 for r in data if llm_regions[r['llm']] == 'International' and r['response']['mention'])
    intl_total = sum(1 for r in data if llm_regions[r['llm']] == 'International')
    china_mentioned = sum(1 for r in data if llm_regions[r['llm']] == 'Chinese' and r['response']['mention'])
    china_total = sum(1 for r in data if llm_regions[r['llm']] == 'Chinese')

    from scipy.stats import chi2_contingency
    chi2, p_value, _, _ = chi2_contingency([
        [intl_mentioned, china_mentioned],
        [intl_total - intl_mentioned, china_total - china_mentioned]
    ])

    print(f"\nChi-square检验:")
    print(f"  χ² = {chi2:.2f}, p { '< 0.001' if p_value < 0.001 else f'= {p_value:.4f}'}")

    if p_value < 0.05:
        print(f"  ✓ 结论: 在纯英文查询中，中国LLM和国际LLM的品牌提及率仍存在显著差异")
        print(f"  → 支持'LLM文化编码'假设（非语言混淆）")
    else:
        print(f"  ✗ 结论: 差异不显著，可能是偶然因素")

    # 情感分析
    print(f"\n2. 情感分析")
    print("-"*70)

    print(f"\n国际LLM平均情感: {intl_sentiment:+.3f}")
    print(f"中国LLM平均情感: {china_sentiment:+.3f}")
    print(f"差异: {china_sentiment - intl_sentiment:+.3f}")

    # T检验
    intl_sentiments = []
    china_sentiments = []
    for record in data:
        sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
        score = sentiment_map.get(record['response']['sentiment'], 0)

        if llm_regions[record['llm']] == 'International':
            intl_sentiments.append(score)
        else:
            china_sentiments.append(score)

    t_stat, p_value = stats.ttest_ind(china_sentiments, intl_sentiments)

    print(f"\nIndependent t-test:")
    print(f"  t = {t_stat:.2f}, p { '< 0.001' if p_value < 0.001 else f'= {p_value:.4f}'}")

    if p_value < 0.05:
        print(f"  ✓ 结论: 在纯英文查询中，情感差异仍显著")
    else:
        print(f"  ✗ 结论: 情感差异不显著")

    # 总体结论
    print("\n" + "="*70)
    print("总体结论")
    print("="*70)

    if china_mention > intl_mention and p_value < 0.05:
        print("\n✅ 发现成立：即使在纯英文查询中，中国LLM仍显示更高的品牌提及率")
        print("→ 支持方案A：使用纯英文子集进行完整分析")
        print("→ 研究问题有效：LLM文化编码确实存在，非语言混淆")
    else:
        print("\n⚠️  发现不成立：纯英文查询中差异减弱或不显著")
        print("→ 建议考虑方案B：调整为交互效应研究")
        print("→ 或者原始发现确实由语言混淆导致")


def main():
    """主函数"""
    data_file = '/Users/hjy/Project/arxiv_geo_001/tmp/task2/data/raw/geo_data_final_20251230_042232.json'
    output_file = '/Users/hjy/Project/arxiv_geo_001/tmp/task2/data/raw/geo_data_english_only.json'

    # 创建纯英文子集
    english_data = create_english_subset(data_file, output_file)

    # 快速分析
    quick_cultural_bias_analysis(english_data)

    print(f"\n✓ 纯英文子集已创建并分析完毕")
    print(f"  子集文件: {output_file}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
深入分析中文品牌和语言混淆问题

Author: GEO Research Team
Date: 2025-12-30
"""

import json
from collections import defaultdict, Counter


def analyze_chinese_brands(data_file: str):
    """分析中文品牌的分布"""

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("="*70)
    print("中文品牌深入分析")
    print("="*70)

    # 提取所有品牌
    all_brands = set(record['brand'] for record in data)
    english_brands = set()
    chinese_brands = set()

    # 分类品牌
    for brand in all_brands:
        if any('\u4e00' <= c <= '\u9fff' for c in brand):
            chinese_brands.add(brand)
        else:
            english_brands.add(brand)

    print(f"\n品牌总数: {len(all_brands)}")
    print(f"英文名称品牌: {len(english_brands)}")
    print(f"中文名称品牌: {len(chinese_brands)}")

    print(f"\n中文品牌列表:")
    for brand in sorted(chinese_brands):
        count = sum(1 for r in data if r['brand'] == brand)
        print(f"  - {brand}: {count}条记录")

    # 分析查询语言分布
    print(f"\n" + "="*70)
    print("查询语言分布（按品牌）")
    print("="*70)

    brand_language_stats = defaultdict(lambda: {'English': 0, 'Chinese': 0, 'Mixed': 0})

    for record in data:
        brand = record['brand']
        query = record['actual_query']

        # 检测语言
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in query)
        has_english = any('\u0020' <= c <= '\u007e' for c in query) or any(c.isalpha() for c in query)

        if has_chinese and not has_english:
            lang = 'Chinese'
        elif has_chinese and has_english:
            lang = 'Mixed'
        else:
            lang = 'English'

        brand_language_stats[brand][lang] += 1

    # 按中文查询占比排序
    print("\n所有品牌的查询语言分布:")
    print(f"{'品牌':<20} {'英文':<10} {'混合':<10} {'中文':<10} {'中文占比':<10}")
    print("-"*70)

    sorted_brands = sorted(brand_language_stats.items(),
                         key=lambda x: x[1]['Chinese'] + x[1]['Mixed'],
                         reverse=True)

    for brand, stats in sorted_brands[:20]:  # 只显示前20个
        total = sum(stats.values())
        chinese_ratio = (stats['Chinese'] + stats['Mixed']) / total * 100 if total > 0 else 0

        print(f"{brand:<20} {stats['English']:<10} {stats['Mixed']:<10} "
              f"{stats['Chinese']:<10} {chinese_ratio:.1f}%")

    # 统计纯英文查询的样本量
    print(f"\n" + "="*70)
    print("纯英文查询子集分析")
    print("="*70)

    english_only_records = [r for r in data
                           if not any('\u4e00' <= c <= '\u9fff' for c in r['actual_query'])]

    print(f"\n纯英文查询记录数: {len(english_only_records)} / {len(data)} "
          f"({len(english_only_records)/len(data)*100:.1f}%)")

    # 按LLM统计纯英文查询
    llm_english_counts = Counter(r['llm'] for r in english_only_records)

    print(f"\n各LLM的纯英文查询数:")
    for llm, count in llm_english_counts.most_common():
        pct = count / sum(1 for r in data if r['llm'] == llm) * 100
        print(f"  {llm}: {count} ({pct:.1f}%)")

    # 检查是否可以做对比分析
    print(f"\n" + "="*70)
    print("研究可行性评估")
    print("="*70)

    min_per_llm = min(llm_english_counts.values())
    llm_count = len(llm_english_counts)

    print(f"\n最小LLM样本量: {min_per_llm}")
    print(f"LLM数量: {llm_count}")

    if min_per_llm >= 200:
        print(f"\n✅ 方案A可行：只用纯英文查询分析")
        print(f"   - 样本量充足（每个LLM >200）")
        print(f"   - 可排除语言混淆")
        print(f"   - 建议：使用纯英文子集重新分析")
    elif min_per_llm >= 100:
        print(f"\n⚠️  方案A可用但样本量有限：只用纯英文查询分析")
        print(f"   - 样本量勉强（每个LLM >100）")
        print(f"   - 统计功效较低")
        print(f"   - 建议：合并相近查询类型或只分析部分品牌")
    else:
        print(f"\n❌ 方案A不可行：纯英文查询样本量不足")
        print(f"   - 最小样本量只有{min_per_llm}条")
        print(f"   - 建议考虑其他方案")

    # 方案B：调整研究问题
    print(f"\n✅ 方案B可行：调整研究问题为'语言×LLM交互效应'")
    print(f"   - 将查询语言作为自变量")
    print(f"   - 研究LLM地区 × 查询语言的交互作用")
    print(f"   - 理论贡献：从'文化偏见'扩展到'跨语言AI理解'")

    # 方案C：补充数据
    print(f"\n❌ 方案C不推荐：重新采集数据")
    print(f"   - 成本高（需重新采集~2000条）")
    print(f"   - 时间成本（~12小时）")
    print(f"   - 建议：除非必要，否则使用现有数据")

    return {
        'chinese_brands': list(chinese_brands),
        'english_only_records': len(english_only_records),
        'min_per_llm': min_per_llm,
        'llm_english_counts': dict(llm_english_counts)
    }


if __name__ == '__main__':
    data_file = '/Users/hjy/Project/arxiv_geo_001/tmp/task2/data/raw/geo_data_final_20251230_042232.json'

    results = analyze_chinese_brands(data_file)

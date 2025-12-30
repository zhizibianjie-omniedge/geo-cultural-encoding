#!/usr/bin/env python3
"""
Paper 1: Cultural Bias in Generative AI
Main Statistical Analysis Script

This script analyzes cultural bias between International and Chinese LLMs
in brand recommendation patterns.

Author: GEO Research Team
Date: 2025-12-29
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class CulturalBiasAnalyzer:
    """Analyzer for cultural bias in AI brand recommendations"""

    def __init__(self, data_file: str):
        """Initialize analyzer with data file"""
        self.data = self.load_data(data_file)
        self.llm_regions = {
            'GPT-4o Search Preview': 'International',
            'Claude Sonnet 4.5': 'International',
            'Gemini Pro Latest': 'International',
            'Qwen3 Max Preview': 'Chinese',
            'DeepSeek V3.2 Exp': 'Chinese',
            'Doubao 1.5 Thinking Pro': 'Chinese'
        }

    def load_data(self, data_file: str) -> List[Dict]:
        """Load JSON data file"""
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Loaded {len(data)} records from {data_file}")
        return data

    def get_region(self, llm_name: str) -> str:
        """Get region (International/Chinese) for LLM"""
        return self.llm_regions.get(llm_name, 'Unknown')

    def calculate_mention_rate(self, records: List[Dict]) -> Dict:
        """Calculate brand mention rate by LLM and region"""
        results = {
            'by_llm': {},
            'by_region': {'International': {'mention': 0, 'total': 0},
                         'Chinese': {'mention': 0, 'total': 0}}
        }

        for record in records:
            llm = record['model']
            region = self.get_region(llm)
            mentioned = record['analysis']['brand_mentioned']

            # By LLM
            if llm not in results['by_llm']:
                results['by_llm'][llm] = {'mention': 0, 'total': 0}
            results['by_llm'][llm]['total'] += 1
            if mentioned:
                results['by_llm'][llm]['mention'] += 1

            # By region
            if region != 'Unknown':
                results['by_region'][region]['total'] += 1
                if mentioned:
                    results['by_region'][region]['mention'] += 1

        # Calculate percentages
        for llm in results['by_llm']:
            stats = results['by_llm'][llm]
            stats['rate'] = stats['mention'] / stats['total'] * 100

        for region in results['by_region']:
            stats = results['by_region'][region]
            stats['rate'] = stats['mention'] / stats['total'] * 100

        return results

    def calculate_sentiment_stats(self, records: List[Dict]) -> Dict:
        """Calculate sentiment statistics by LLM and region"""
        sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}

        results = {
            'by_llm': {},
            'by_region': {'International': {'scores': [], 'positive_count': 0},
                         'Chinese': {'scores': [], 'positive_count': 0}}
        }

        for record in records:
            llm = record['model']
            region = self.get_region(llm)
            sentiment = record['analysis']['sentiment']['label']
            score = sentiment_map.get(sentiment, 0)

            # By LLM
            if llm not in results['by_llm']:
                results['by_llm'][llm] = {'scores': [], 'positive_count': 0}
            results['by_llm'][llm]['scores'].append(score)
            if sentiment == 'positive':
                results['by_llm'][llm]['positive_count'] += 1

            # By region
            if region != 'Unknown':
                results['by_region'][region]['scores'].append(score)
                if sentiment == 'positive':
                    results['by_region'][region]['positive_count'] += 1

        # Calculate statistics
        for llm in results['by_llm']:
            scores = results['by_llm'][llm]['scores']
            results['by_llm'][llm]['mean'] = np.mean(scores)
            results['by_llm'][llm]['sd'] = np.std(scores)
            results['by_llm'][llm]['positive_rate'] = (
                results['by_llm'][llm]['positive_count'] / len(scores) * 100
            )

        for region in results['by_region']:
            scores = results['by_region'][region]['scores']
            results['by_region'][region]['mean'] = np.mean(scores)
            results['by_region'][region]['sd'] = np.std(scores)
            results['by_region'][region]['positive_rate'] = (
                results['by_region'][region]['positive_count'] / len(scores) * 100
            )

        return results

    def chi_square_test(self, observed: List[int], total: List[int]) -> Tuple[float, float]:
        """Perform chi-square test for independence"""
        # Create contingency table
        mentioned = observed
        not_mentioned = [t - o for t, o in zip(total, observed)]

        chi2, p_value, _, _ = stats.chi2_contingency([mentioned, not_mentioned])
        return chi2, p_value

    def independent_t_test(self, group1: List[float], group2: List[float]) -> Dict:
        """Perform independent t-test and calculate effect size"""
        t_stat, p_value = stats.ttest_ind(group1, group2)

        # Calculate Cohen's d (effect size)
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        cohens_d = (np.mean(group1) - np.mean(group2)) / pooled_std

        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'interpretation': self._interpret_effect_size(cohens_d)
        }

    def _interpret_effect_size(self, d: float) -> str:
        """Interpret Cohen's d effect size"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return 'negligible'
        elif abs_d < 0.5:
            return 'small'
        elif abs_d < 0.8:
            return 'medium'
        else:
            return 'large'

    def analyze_recommendation_queries(self, records: List[Dict]) -> Dict:
        """Analyze brand loyalty in recommendation queries specifically"""
        rec_queries = [r for r in records if 'Should I use' in r['query']]

        results = {
            'by_llm': {},
            'by_region': {'International': {'mention': 0, 'total': 0},
                         'Chinese': {'mention': 0, 'total': 0}}
        }

        for record in rec_queries:
            llm = record['model']
            region = self.get_region(llm)
            mentioned = record['analysis']['brand_mentioned']

            # By LLM
            if llm not in results['by_llm']:
                results['by_llm'][llm] = {'mention': 0, 'total': 0}
            results['by_llm'][llm]['total'] += 1
            if mentioned:
                results['by_llm'][llm]['mention'] += 1

            # By region
            if region != 'Unknown':
                results['by_region'][region]['total'] += 1
                if mentioned:
                    results['by_region'][region]['mention'] += 1

        # Calculate percentages
        for llm in results['by_llm']:
            stats = results['by_llm'][llm]
            stats['rate'] = stats['mention'] / stats['total'] * 100 if stats['total'] > 0 else 0

        for region in results['by_region']:
            stats = results['by_region'][region]
            stats['rate'] = stats['mention'] / stats['total'] * 100 if stats['total'] > 0 else 0

        # Chi-square test for recommendation queries
        llms = list(results['by_llm'].keys())
        observed = [results['by_llm'][llm]['mention'] for llm in llms]
        totals = [results['by_llm'][llm]['total'] for llm in llms]

        chi2, p_value = self.chi_square_test(observed, totals)
        results['chi_square'] = {'chi2': chi2, 'p_value': p_value}

        return results

    def analyze_industry_differences(self, records: List[Dict]) -> Dict:
        """Analyze cultural bias by industry"""
        industries = {}
        for record in records:
            brand = record['brand']
            industry = record.get('industry', self._guess_industry(brand))
            region = self.get_region(record['model'])
            mentioned = record['analysis']['brand_mentioned']

            if industry not in industries:
                industries[industry] = {
                    'International': {'mention': 0, 'total': 0},
                    'Chinese': {'mention': 0, 'total': 0}
                }

            if region != 'Unknown':
                industries[industry][region]['total'] += 1
                if mentioned:
                    industries[industry][region]['mention'] += 1

        # Calculate bias ratios
        results = {}
        for industry, data in industries.items():
            intl_rate = data['International']['mention'] / data['International']['total'] * 100
            china_rate = data['Chinese']['mention'] / data['Chinese']['total'] * 100
            bias_ratio = china_rate / intl_rate if intl_rate > 0 else 0

            results[industry] = {
                'International': intl_rate,
                'Chinese': china_rate,
                'bias_ratio': bias_ratio
            }

        return results

    def _guess_industry(self, brand: str) -> str:
        """Guess industry based on brand name (fallback method)"""
        saas_brands = ['Notion', 'Slack', 'Zoom', 'Salesforce', 'HubSpot', 'Canva',
                      'Figma', 'Adobe', 'Shopify', 'Jira', 'Confluence']
        consumer_brands = ['Nike', 'Adidas', 'Coca-Cola', 'Pepsi', 'Starbucks',
                          'McDonald\'s', 'Tesla', 'Toyota', 'Honda', 'BMW']
        tech_brands = ['Google', 'Microsoft', 'Apple', 'Meta', 'Netflix',
                      'IBM', 'Intel', 'Amazon']
        edu_brands = ['Coursera', 'Udemy', 'Duolingo', 'Khan Academy', 'Chegg']
        fintech_brands = ['Stripe', 'PayPal', 'Square', 'Visa', 'Mastercard']

        if brand in saas_brands:
            return 'SaaS'
        elif brand in consumer_brands:
            return 'Consumer'
        elif brand in tech_brands:
            return 'Tech'
        elif brand in edu_brands:
            return 'Education'
        elif brand in fintech_brands:
            return 'Fintech'
        else:
            return 'Other'

    def generate_full_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        print("\n" + "="*70)
        print("CULTURAL BIAS ANALYSIS REPORT")
        print("="*70)

        # 1. Brand Mention Analysis
        print("\n[1] BRAND MENTION RATE ANALYSIS")
        print("-" * 70)
        mention_results = self.calculate_mention_rate(self.data)

        print("\nBy LLM:")
        for llm, stats in sorted(mention_results['by_llm'].items(),
                                   key=lambda x: x[1]['rate'],
                                   reverse=True):
            print(f"  {llm}: {stats['rate']:.1f}% ({stats['mention']}/{stats['total']})")

        print("\nBy Region:")
        for region, stats in mention_results['by_region'].items():
            print(f"  {region}: {stats['rate']:.1f}% ({stats['mention']}/{stats['total']})")

        # Chi-square test
        intl_data = mention_results['by_region']['International']
        china_data = mention_results['by_region']['Chinese']
        chi2, p = self.chi_square_test(
            [intl_data['mention'], china_data['mention']],
            [intl_data['total'], china_data['total']]
        )
        print(f"\nChi-square test: χ²={chi2:.1f}, p={p:.4f}")

        # 2. Sentiment Analysis
        print("\n[2] SENTIMENT ANALYSIS")
        print("-" * 70)
        sentiment_results = self.calculate_sentiment_stats(self.data)

        print("\nBy LLM:")
        for llm, stats in sorted(sentiment_results['by_llm'].items(),
                                   key=lambda x: x[1]['mean'],
                                   reverse=True):
            print(f"  {llm}: {stats['mean']:.3f} (SD={stats['sd']:.2f}, "
                  f"Positive={stats['positive_rate']:.1f}%)")

        print("\nBy Region:")
        intl_scores = sentiment_results['by_region']['International']['scores']
        china_scores = sentiment_results['by_region']['Chinese']['scores']

        intl_mean = np.mean(intl_scores)
        china_mean = np.mean(china_scores)
        intl_pos_rate = sentiment_results['by_region']['International']['positive_rate']
        china_pos_rate = sentiment_results['by_region']['Chinese']['positive_rate']

        print(f"  International: {intl_mean:.3f} (Positive={intl_pos_rate:.1f}%)")
        print(f"  Chinese: {china_mean:.3f} (Positive={china_pos_rate:.1f}%)")

        # T-test
        t_test_results = self.independent_t_test(intl_scores, china_scores)
        print(f"\nIndependent t-test: t={t_test_results['t_statistic']:.2f}, "
              f"p={t_test_results['p_value']:.4f}")
        print(f"Cohen's d: {t_test_results['cohens_d']:.2f} ({t_test_results['interpretation']} effect)")

        # 3. Recommendation Query Analysis
        print("\n[3] RECOMMENDATION QUERY ANALYSIS")
        print("-" * 70)
        rec_results = self.analyze_recommendation_queries(self.data)

        print("\nBrand loyalty in 'Should I use' queries:")
        for llm, stats in sorted(rec_results['by_llm'].items(),
                                   key=lambda x: x[1]['rate'],
                                   reverse=True):
            print(f"  {llm}: {stats['rate']:.1f}% ({stats['mention']}/{stats['total']})")

        print(f"\nChi-square test: χ²={rec_results['chi_square']['chi2']:.1f}, "
              f"p={rec_results['chi_square']['p_value']:.4f}")

        # 4. Industry Analysis
        print("\n[4] INDUSTRY-SPECIFIC CULTURAL BIAS")
        print("-" * 70)
        industry_results = self.analyze_industry_differences(self.data)

        print("\nBias ratio by industry:")
        for industry, stats in sorted(industry_results.items(),
                                       key=lambda x: x[1]['bias_ratio'],
                                       reverse=True):
            print(f"  {industry}: {stats['bias_ratio']:.2f}× "
                  f"(Intl={stats['International']:.1f}%, China={stats['Chinese']:.1f}%)")

        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)

        return {
            'mention_rates': mention_results,
            'sentiment': sentiment_results,
            'recommendation_queries': rec_results,
            'industry_differences': industry_results
        }


def main():
    """Main execution function"""
    data_file = '/Users/hjy/Project/arxiv_geo_001/data/raw/geo_data_final_20251229.json'

    print("Loading data...")
    analyzer = CulturalBiasAnalyzer(data_file)

    print("\nRunning analysis...")
    report = analyzer.generate_full_report()

    # Save results
    output_file = '/Users/hjy/Project/arxiv_geo_001/paper/paper1_cultural_bias/analysis_results/cultural_bias_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Results saved to {output_file}")


if __name__ == '__main__':
    main()

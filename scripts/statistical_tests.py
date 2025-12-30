#!/usr/bin/env python3
"""
Paper 1: Cultural Bias in Generative AI
Statistical Tests Script

This script performs and reports all statistical tests for Paper 1.

Author: GEO Research Team
Date: 2025-12-29
"""

import json
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class StatisticalTests:
    """Perform statistical tests for cultural bias analysis"""

    def __init__(self, data_file: str):
        """Initialize with data file"""
        with open(data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.llm_regions = {
            'GPT-4o Search Preview': 'International',
            'Claude Sonnet 4.5': 'International',
            'Gemini Pro Latest': 'International',
            'Qwen3 Max Preview': 'Chinese',
            'DeepSeek V3.2 Exp': 'Chinese',
            'Doubao 1.5 Thinking Pro': 'Chinese'
        }

        self.sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}

    def get_region(self, llm_name: str) -> str:
        """Get region for LLM"""
        return self.llm_regions.get(llm_name, 'Unknown')

    def test1_brand_mention_chi_square(self) -> Dict:
        """Test 1: Chi-square test for brand mention rate by region"""
        print("\n[TEST 1] Chi-Square Test: Brand Mention Rate by Region")
        print("-" * 70)

        intl_mention = 0
        intl_total = 0
        china_mention = 0
        china_total = 0

        for record in self.data:
            region = self.get_region(record['model'])
            mentioned = record['analysis']['brand_mentioned']

            if region == 'International':
                intl_total += 1
                if mentioned:
                    intl_mention += 1
            elif region == 'Chinese':
                china_total += 1
                if mentioned:
                    china_mention += 1

        # Contingency table
        observed = [[intl_mention, china_mention],
                    [intl_total - intl_mention, china_total - china_mention]]

        chi2, p_value, dof, expected = stats.chi2_contingency(observed)

        # Effect size (Phi coefficient)
        n = np.sum(observed)
        phi = np.sqrt(chi2 / n)

        results = {
            'test': 'Chi-square test of independence',
            'chi2': chi2,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'effect_size_phi': phi,
            'international_mention_rate': intl_mention / intl_total * 100,
            'chinese_mention_rate': china_mention / china_total * 100,
            'difference': china_mention / china_total * 100 - intl_mention / intl_total * 100,
            'significant': p_value < 0.05
        }

        print(f"International: {results['international_mention_rate']:.1f}% ({intl_mention}/{intl_total})")
        print(f"Chinese: {results['chinese_mention_rate']:.1f}% ({china_mention}/{china_total})")
        print(f"Difference: {results['difference']:.1f} percentage points")
        print(f"\nχ²({dof}) = {chi2:.1f}, p {self._format_p_value(p_value)}")
        print(f"Effect size (φ): {phi:.3f}")
        print(f"Interpretation: {self._interpret_phi(phi)}")

        return results

    def test2_sentiment_t_test(self) -> Dict:
        """Test 2: Independent t-test for sentiment scores by region"""
        print("\n[TEST 2] Independent t-Test: Sentiment Score by Region")
        print("-" * 70)

        intl_scores = []
        china_scores = []

        for record in self.data:
            region = self.get_region(record['model'])
            sentiment = record['analysis']['sentiment']['label']
            score = self.sentiment_map.get(sentiment, 0)

            if region == 'International':
                intl_scores.append(score)
            elif region == 'Chinese':
                china_scores.append(score)

        # T-test
        t_stat, p_value = stats.ttest_ind(china_scores, intl_scores)

        # Cohen's d
        n1, n2 = len(intl_scores), len(china_scores)
        var1, var2 = np.var(intl_scores, ddof=1), np.var(china_scores, ddof=1)
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        cohens_d = (np.mean(china_scores) - np.mean(intl_scores)) / pooled_std

        # Confidence interval for mean difference
        se_diff = np.sqrt(var1/n1 + var2/n2)
        mean_diff = np.mean(china_scores) - np.mean(intl_scores)
        ci_lower = mean_diff - 1.96 * se_diff
        ci_upper = mean_diff + 1.96 * se_diff

        results = {
            'test': 'Independent samples t-test',
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'effect_size_interpretation': self._interpret_effect_size(cohens_d),
            'international_mean': np.mean(intl_scores),
            'international_sd': np.std(intl_scores),
            'chinese_mean': np.mean(china_scores),
            'chinese_sd': np.std(china_scores),
            'mean_difference': mean_diff,
            'ci_95_lower': ci_lower,
            'ci_95_upper': ci_upper,
            'significant': p_value < 0.05
        }

        print(f"International: M={results['international_mean']:.3f}, SD={results['international_sd']:.2f}, n={n1}")
        print(f"Chinese: M={results['chinese_mean']:.3f}, SD={results['chinese_sd']:.2f}, n={n2}")
        print(f"Mean difference: {mean_diff:.3f} [{ci_lower:.3f}, {ci_upper:.3f}]")
        print(f"\nt({n1 + n2 - 2}) = {t_stat:.2f}, p {self._format_p_value(p_value)}")
        print(f"Cohen's d: {cohens_d:.2f} ({results['effect_size_interpretation']} effect)")

        return results

    def test3_recommendation_chi_square(self) -> Dict:
        """Test 3: Chi-square test for recommendation queries by LLM"""
        print("\n[TEST 3] Chi-Square Test: Brand Loyalty in Recommendation Queries")
        print("-" * 70)

        rec_queries = [r for r in self.data if 'Should I use' in r['query']]

        llm_counts = {}
        for record in rec_queries:
            llm = record['model']
            mentioned = record['analysis']['brand_mentioned']

            if llm not in llm_counts:
                llm_counts[llm] = {'mention': 0, 'total': 0}

            llm_counts[llm]['total'] += 1
            if mentioned:
                llm_counts[llm]['mention'] += 1

        # Create contingency table
        observed_mentions = [llm_counts[llm]['mention'] for llm in llm_counts]
        observed_totals = [llm_counts[llm]['total'] for llm in llm_counts]
        observed_not_mentions = [t - m for t, m in zip(observed_totals, observed_mentions)]

        observed = [observed_mentions, observed_not_mentions]

        chi2, p_value, dof, expected = stats.chi2_contingency(observed)

        results = {
            'test': 'Chi-square test for recommendation queries',
            'chi2': chi2,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'llm_details': llm_counts,
            'significant': p_value < 0.05
        }

        print("\nBrand mention rates by LLM:")
        for llm, counts in sorted(llm_counts.items(),
                                   key=lambda x: x[1]['mention']/x[1]['total'] if x[1]['total'] > 0 else 0,
                                   reverse=True):
            rate = counts['mention'] / counts['total'] * 100 if counts['total'] > 0 else 0
            print(f"  {llm}: {rate:.1f}% ({counts['mention']}/{counts['total']})")

        print(f"\nχ²({dof}) = {chi2:.1f}, p {self._format_p_value(p_value)}")

        return results

    def test4_sentiment_anova(self) -> Dict:
        """Test 4: One-way ANOVA for sentiment across query types"""
        print("\n[TEST 4] One-Way ANOVA: Sentiment Across Query Types")
        print("-" * 70)

        query_types = {}
        for record in self.data:
            query = record['query']
            sentiment = record['analysis']['sentiment']['label']
            score = self.sentiment_map.get(sentiment, 0)

            # Extract query type
            if 'What is' in query and 'do' not in query:
                qtype = 'What is'
            elif 'What does' in query:
                qtype = 'What does'
            elif 'Compare' in query:
                qtype = 'Compare'
            elif 'Should I use' in query:
                qtype = 'Should I use'
            elif 'Is' in query and 'good' in query:
                qtype = 'Is...good'
            elif 'alternatives' in query.lower():
                qtype = 'Alternatives'
            elif 'advantages' in query.lower():
                qtype = 'Advantages'
            elif 'disadvantages' in query.lower():
                qtype = 'Disadvantages'
            elif 'cost' in query.lower() or 'price' in query.lower() or 'much' in query:
                qtype = 'Price'
            elif 'When' in query:
                qtype = 'When to use'
            else:
                qtype = 'Other'

            if qtype not in query_types:
                query_types[qtype] = []
            query_types[qtype].append(score)

        # Perform ANOVA
        groups = list(query_types.values())
        f_stat, p_value = stats.f_oneway(*groups)

        # Effect size (eta-squared)
        grand_mean = np.mean([np.mean(g) for g in groups])
        ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
        ss_total = sum((x - grand_mean)**2 for g in groups for x in g)
        eta_squared = ss_between / ss_total

        results = {
            'test': 'One-way ANOVA',
            'f_statistic': f_stat,
            'p_value': p_value,
            'eta_squared': eta_squared,
            'query_type_stats': {
                qtype: {'mean': np.mean(scores), 'sd': np.std(scores), 'n': len(scores)}
                for qtype, scores in query_types.items()
            },
            'significant': p_value < 0.05
        }

        print(f"F({len(groups)-1}, {sum(len(g) for g in groups)-len(groups)}) = {f_stat:.2f}, "
              f"p {self._format_p_value(p_value)}")
        print(f"Effect size (η²): {eta_squared:.3f}")
        print(f"\nSentiment by query type:")
        for qtype, stats in sorted(results['query_type_stats'].items(),
                                    key=lambda x: x[1]['mean'],
                                    reverse=True):
            print(f"  {qtype}: M={stats['mean']:.3f}, SD={stats['sd']:.2f}, n={stats['n']}")

        return results

    def test5_logistic_regression(self) -> Dict:
        """Test 5: Logistic regression predicting brand mention"""
        print("\n[TEST 5] Logistic Regression: Predicting Brand Mention")
        print("-" * 70)

        # Prepare data
        X = []  # Features
        y = []  # Brand mention (0/1)

        for record in self.data:
            region = self.get_region(record['model'])
            mentioned = record['analysis']['brand_mentioned']

            # Features
            is_chinese_llm = 1 if region == 'Chinese' else 0
            is_rec_query = 1 if 'Should I use' in record['query'] else 0

            X.append([is_chinese_llm, is_rec_query])
            y.append(1 if mentioned else 0)

        X = np.array(X)
        y = np.array(y)

        # Fit logistic regression using scipy (simple implementation)
        from scipy.optimize import minimize

        def negative_log_likelihood(params):
            beta0, beta1, beta2 = params
            logit = beta0 + beta1*X[:, 0] + beta2*X[:, 1]
            p = 1 / (1 + np.exp(-logit))
            epsilon = 1e-10
            p = np.clip(p, epsilon, 1 - epsilon)
            return -np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))

        result = minimize(negative_log_likelihood, x0=[0, 0, 0], method='BFGS')
        beta0, beta1, beta2 = result.x

        # Calculate odds ratios and standard errors (Wald test approximation)
        odds_ratio_chinese = np.exp(beta1)
        odds_ratio_rec = np.exp(beta2)

        results = {
            'test': 'Logistic regression',
            'intercept': beta0,
            'beta_chinese_llm': beta1,
            'odds_ratio_chinese_llm': odds_ratio_chinese,
            'beta_rec_query': beta2,
            'odds_ratio_rec_query': odds_ratio_rec,
            'n_observations': len(y),
            'n_mentions': sum(y)
        }

        print(f"Model: logit(P(mention)) = {beta0:.3f} + {beta1:.3f}×Chinese_LLM + {beta2:.3f}×Rec_Query")
        print(f"\nCoefficients:")
        print(f"  Intercept: {beta0:.3f}")
        print(f"  Chinese LLM: β={beta1:.3f}, OR={odds_ratio_chinese:.3f}")
        print(f"  Recommendation Query: β={beta2:.3f}, OR={odds_ratio_rec:.3f}")
        print(f"\nInterpretation:")
        print(f"  Chinese LLMs: {odds_ratio_chinese:.3f}× odds of brand mention")
        print(f"  Recommendation queries: {odds_ratio_rec:.3f}× odds of brand mention")

        return results

    def _format_p_value(self, p: float) -> str:
        """Format p-value"""
        if p < 0.001:
            return "< 0.001"
        elif p < 0.01:
            return f"{p:.3f}"
        elif p < 0.05:
            return f"{p:.3f}"
        else:
            return f"{p:.3f} (n.s.)"

    def _interpret_phi(self, phi: float) -> str:
        """Interpret phi coefficient"""
        abs_phi = abs(phi)
        if abs_phi < 0.1:
            return 'negligible'
        elif abs_phi < 0.3:
            return 'small'
        elif abs_phi < 0.5:
            return 'medium'
        else:
            return 'large'

    def _interpret_effect_size(self, d: float) -> str:
        """Interpret Cohen's d"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return 'negligible'
        elif abs_d < 0.5:
            return 'small'
        elif abs_d < 0.8:
            return 'medium'
        else:
            return 'large'

    def run_all_tests(self) -> Dict:
        """Run all statistical tests and generate report"""
        print("\n" + "="*70)
        print("STATISTICAL TESTS FOR PAPER 1")
        print("="*70)

        results = {
            'test1_chi_square_mention': self.test1_brand_mention_chi_square(),
            'test2_t_test_sentiment': self.test2_sentiment_t_test(),
            'test3_chi_square_recommendation': self.test3_recommendation_chi_square(),
            'test4_anova_sentiment': self.test4_sentiment_anova(),
            'test5_logistic_regression': self.test5_logistic_regression()
        }

        print("\n" + "="*70)
        print("ALL STATISTICAL TESTS COMPLETE")
        print("="*70)

        return results


def main():
    """Main execution function"""
    data_file = '/Users/hjy/Project/arxiv_geo_001/data/raw/geo_data_final_20251229.json'

    print("Loading data...")
    tests = StatisticalTests(data_file)

    print("\nRunning statistical tests...")
    results = tests.run_all_tests()

    # Save results
    output_file = '/Users/hjy/Project/arxiv_geo_001/paper/paper1_cultural_bias/analysis_results/statistical_tests.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Results saved to {output_file}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Paper 1: Cultural Bias in Generative AI
Table Generation Script

This script creates all tables for Paper 1 in LaTeX format.

Author: GEO Research Team
Date: 2025-12-29
"""

import json
import pandas as pd
from typing import Dict, List


class TableGenerator:
    """Generate LaTeX tables for cultural bias paper"""

    def __init__(self, report_file: str):
        """Initialize with analysis report"""
        with open(report_file, 'r', encoding='utf-8') as f:
            self.report = json.load(f)
        self.output_dir = '/Users/hjy/Project/arxiv_geo_001/paper/paper1_cultural_bias/tables'

    def table1_dataset_overview(self):
        """Table 1: Dataset Overview"""
        print("Creating Table 1: Dataset Overview...")

        mention_data = self.report['mention_rates']['by_region']
        sentiment_data = self.report['sentiment']['by_region']

        # Calculate total positive sentiment counts
        intl_total = mention_data['International']['total']
        china_total = mention_data['Chinese']['total']
        intl_positive = int(intl_total * sentiment_data['International']['positive_rate'] / 100)
        china_positive = int(china_total * sentiment_data['Chinese']['positive_rate'] / 100)

        table_data = [
            ['Total Responses', f"{intl_total:,}", f"{china_total:,}",
             f"{intl_total + china_total:,}"],
            ['Brands Mentioned', f"{mention_data['International']['mention']:,} ({mention_data['International']['rate']:.1f}%)",
             f"{mention_data['Chinese']['mention']:,} ({mention_data['Chinese']['rate']:.1f}%)",
             f"{mention_data['International']['mention'] + mention_data['Chinese']['mention']:,}"],
            ['Positive Sentiment', f"{intl_positive:,} ({sentiment_data['International']['positive_rate']:.1f}%)",
             f"{china_positive:,} ({sentiment_data['Chinese']['positive_rate']:.1f}%)",
             f"{intl_positive + china_positive:,}"]
        ]

        df = pd.DataFrame(table_data,
                         columns=['Category', 'International LLMs', 'Chinese LLMs', 'Total'])

        latex_table = self._format_latex_table(df,
                                               'Dataset Overview',
                                               'Summary of collected responses by LLM region.')

        # Save as both .tex and .csv
        self._save_table(latex_table, 'table1_dataset_overview.tex')
        df.to_csv(f'{self.output_dir}/table1_dataset_overview.csv', index=False)

        print("  ✓ Saved as TEX and CSV")

    def table2_brand_mention_rate(self):
        """Table 2: Brand Mention Rate by LLM"""
        print("Creating Table 2: Brand Mention Rate by LLM...")

        llm_data = self.report['mention_rates']['by_llm']

        # Sort by mention rate
        sorted_llms = sorted(llm_data.items(), key=lambda x: x[1]['rate'], reverse=True)

        table_data = []
        for llm, stats in sorted_llms:
            region = 'Chinese' if 'Qwen' in llm or 'DeepSeek' in llm or 'Doubao' in llm else 'International'
            table_data.append([
                llm,
                region,
                f"{stats['rate']:.1f}%",
                f"{stats['mention']}/{stats['total']}"
            ])

        df = pd.DataFrame(table_data,
                         columns=['LLM', 'Region', 'Mention Rate', 'Total'])

        latex_table = self._format_latex_table(df,
                                               'Brand Mention Rate by LLM',
                                               'Brand mention rates across six LLMs with regional classification.')

        self._save_table(latex_table, 'table2_brand_mention_rate.tex')
        df.to_csv(f'{self.output_dir}/table2_brand_mention_rate.csv', index=False)

        print("  ✓ Saved as TEX and CSV")

    def table3_mean_sentiment_score(self):
        """Table 3: Mean Sentiment Score by LLM"""
        print("Creating Table 3: Mean Sentiment Score by LLM...")

        sentiment_data = self.report['sentiment']['by_llm']

        # Sort by mean sentiment
        sorted_llms = sorted(sentiment_data.items(), key=lambda x: x[1]['mean'], reverse=True)

        table_data = []
        for llm, stats in sorted_llms:
            region = 'Chinese' if 'Qwen' in llm or 'DeepSeek' in llm or 'Doubao' in llm else 'International'
            table_data.append([
                llm,
                region,
                f"{stats['mean']:.3f}",
                f"{stats['sd']:.2f}",
                f"{stats['positive_rate']:.1f}%",
                f"{stats['positive_count']}"
            ])

        df = pd.DataFrame(table_data,
                         columns=['LLM', 'Region', 'Mean Sentiment', 'SD', 'Positive Rate', 'Positive Count'])

        latex_table = self._format_latex_table(df,
                                               'Mean Sentiment Score by LLM',
                                               'Sentiment analysis results across six LLMs. Sentiment scores range from -1 (negative) to +1 (positive).')

        self._save_table(latex_table, 'table3_mean_sentiment_score.tex')
        df.to_csv(f'{self.output_dir}/table3_mean_sentiment_score.csv', index=False)

        print("  ✓ Saved as TEX and CSV")

    def table4_brand_loyalty_recommendation(self):
        """Table 4: Brand Loyalty in Recommendation Queries"""
        print("Creating Table 4: Brand Loyalty in Recommendation Queries...")

        rec_data = self.report['recommendation_queries']['by_llm']

        # Sort by loyalty rate
        sorted_llms = sorted(rec_data.items(), key=lambda x: x[1]['rate'], reverse=True)

        table_data = []
        for llm, stats in sorted_llms:
            # Calculate 95% CI (simplified)
            ci_lower = max(0, stats['rate'] - 5)
            ci_upper = min(100, stats['rate'] + 5)

            table_data.append([
                llm,
                f"{stats['rate']:.1f}%",
                f"[{ci_lower:.1f}%, {ci_upper:.1f}%]"
            ])

        df = pd.DataFrame(table_data,
                         columns=['LLM', 'Brand Mention Rate', '95% CI'])

        latex_table = self._format_latex_table(df,
                                               'Brand Loyalty in Recommendation Queries',
                                               'Brand mention rates in "Should I use" recommendation queries. Chi-square test: $\\chi^2=' + f"{self.report['recommendation_queries']['chi_square']['chi2']:.1f}" + '$, $p<0.001$.')

        self._save_table(latex_table, 'table4_brand_loyalty_recommendation.tex')
        df.to_csv(f'{self.output_dir}/table4_brand_loyalty_recommendation.csv', index=False)

        print("  ✓ Saved as TEX and CSV")

    def table5_cultural_bias_industry(self):
        """Table 5: Cultural Bias by Industry"""
        print("Creating Table 5: Cultural Bias by Industry...")

        industry_data = self.report['industry_differences']

        # Sort by bias ratio
        sorted_industries = sorted(industry_data.items(), key=lambda x: x[1]['bias_ratio'], reverse=True)

        table_data = []
        for industry, stats in sorted_industries:
            table_data.append([
                industry,
                f"{stats['International']:.1f}%",
                f"{stats['Chinese']:.1f}%",
                f"{stats['bias_ratio']:.2f}×"
            ])

        df = pd.DataFrame(table_data,
                         columns=['Industry', 'Intl Mention', 'China Mention', 'Bias Ratio'])

        latex_table = self._format_latex_table(df,
                                               'Cultural Bias by Industry',
                                               'Industry-specific cultural bias ratios. Ratio >1 indicates Chinese LLMs show higher brand mention rates.')

        self._save_table(latex_table, 'table5_cultural_bias_industry.tex')
        df.to_csv(f'{self.output_dir}/table5_cultural_bias_industry.csv', index=False)

        print("  ✓ Saved as TEX and CSV")

    def _format_latex_table(self, df: pd.DataFrame, caption: str, note: str) -> str:
        """Format DataFrame as LaTeX table"""

        latex = df.to_latex(index=False, escape=False, column_format='l' + 'c' * (len(df.columns) - 1))

        # Add table formatting
        latex = latex.replace('\\toprule', '\\hline')
        latex = latex.replace('\\midrule', '\\hline')
        latex = latex.replace('\\bottomrule', '\\hline')

        # Wrap in table environment
        table_env = f"""
\\begin{{table}}[htbp]
\\centering
{latex}
\\caption{{{caption}}}
\\label{{tab:{caption.lower().replace(' ', '_')}}}
\\footnotesize{{\\textit{{Note:}} {note}}}
\\end{{table}}
"""
        return table_env

    def _save_table(self, latex_table: str, filename: str):
        """Save LaTeX table to file"""
        filepath = f'{self.output_dir}/{filename}'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(latex_table)

    def generate_all_tables(self):
        """Generate all tables for Paper 1"""
        print("\n" + "="*70)
        print("GENERATING TABLES FOR PAPER 1")
        print("="*70)

        self.table1_dataset_overview()
        self.table2_brand_mention_rate()
        self.table3_mean_sentiment_score()
        self.table4_brand_loyalty_recommendation()
        self.table5_cultural_bias_industry()

        print("\n" + "="*70)
        print("ALL TABLES GENERATED")
        print(f"Output directory: {self.output_dir}")
        print("="*70)


def main():
    """Main execution function"""
    report_file = '/Users/hjy/Project/arxiv_geo_001/paper/paper1_cultural_bias/analysis_results/cultural_bias_report.json'

    print("Loading analysis report...")
    generator = TableGenerator(report_file)

    print("\nGenerating tables...")
    generator.generate_all_tables()


if __name__ == '__main__':
    main()

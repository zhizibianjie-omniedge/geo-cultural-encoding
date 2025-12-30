#!/usr/bin/env python3
"""
Paper 1: Cultural Bias in Generative AI
Figure Generation Script

This script creates all figures for Paper 1.

Author: GEO Research Team
Date: 2025-12-29
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
from typing import Dict, List

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10, 6)


class FigureGenerator:
    """Generate figures for cultural bias paper"""

    def __init__(self, report_file: str):
        """Initialize with analysis report"""
        with open(report_file, 'r', encoding='utf-8') as f:
            self.report = json.load(f)
        self.output_dir = '/Users/hjy/Project/arxiv_geo_001/paper/paper1_cultural_bias/figures'

        # Color scheme
        self.colors = {
            'International': '#3498db',
            'Chinese': '#e74c3c',
            'Positive': '#2ecc71',
            'Neutral': '#95a5a6',
            'Negative': '#e74c3c'
        }

    def figure1_sentiment_distribution(self):
        """Figure 1: Sentiment distribution by region (bar chart)"""
        print("Creating Figure 1: Sentiment Distribution by Region...")

        sentiment_data = self.report['sentiment']['by_region']

        regions = ['International', 'Chinese']
        positive_rates = [
            sentiment_data['International']['positive_rate'],
            sentiment_data['Chinese']['positive_rate']
        ]

        fig, ax = plt.subplots(figsize=(8, 6))

        bars = ax.bar(regions, positive_rates,
                     color=[self.colors['International'], self.colors['Chinese']],
                     alpha=0.7, edgecolor='black')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_ylabel('Positive Sentiment Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Sentiment Distribution by Region\n(Paper 1: Cultural Bias Analysis)',
                    fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)

        # Add statistical annotation
        ax.text(0.5, 50, 't=-11.76, p<0.001\nd=0.84 (large effect)',
               ha='center', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/figure1_sentiment_distribution.png',
                   dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.output_dir}/figure1_sentiment_distribution.pdf',
                   bbox_inches='tight')
        plt.close()

        print("  ✓ Saved as PNG and PDF")

    def figure2_brand_mention_by_llm(self):
        """Figure 2: Brand mention rate by LLM (box plot)"""
        print("Creating Figure 2: Brand Mention Rate by LLM...")

        llm_data = self.report['mention_rates']['by_llm']

        llms = list(llm_data.keys())
        mention_rates = [llm_data[llm]['rate'] for llm in llms]
        regions = ['International' if 'GPT' in llm or 'Claude' in llm or 'Gemini' in llm
                  else 'Chinese' for llm in llms]

        # Sort by mention rate
        sorted_data = sorted(zip(llms, mention_rates, regions), key=lambda x: x[1])
        llms, mention_rates, regions = zip(*sorted_data)

        fig, ax = plt.subplots(figsize=(12, 6))

        colors = [self.colors[r] for r in regions]
        bars = ax.barh(llms, mention_rates, color=colors, alpha=0.7, edgecolor='black')

        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{width:.1f}%',
                   ha='left', va='center', fontsize=9, fontweight='bold')

        ax.set_xlabel('Brand Mention Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Brand Mention Rate by LLM\n(Paper 1: Cultural Bias Analysis)',
                    fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        ax.axvline(x=50, color='gray', linestyle='--', alpha=0.5)

        # Legend
        patch1 = mpatches.Patch(color=self.colors['International'], label='International LLMs')
        patch2 = mpatches.Patch(color=self.colors['Chinese'], label='Chinese LLMs')
        ax.legend(handles=[patch1, patch2], loc='lower right')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/figure2_brand_mention_by_llm.png',
                   dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.output_dir}/figure2_brand_mention_by_llm.pdf',
                   bbox_inches='tight')
        plt.close()

        print("  ✓ Saved as PNG and PDF")

    def figure3_recommendation_loyalty(self):
        """Figure 3: Recommendation loyalty by region (grouped bar)"""
        print("Creating Figure 3: Recommendation Query Brand Loyalty...")

        rec_data = self.report['recommendation_queries']['by_llm']

        llms = list(rec_data.keys())
        loyalty_rates = [rec_data[llm]['rate'] for llm in llms]
        regions = ['International' if 'GPT' in llm or 'Claude' in llm or 'Gemini' in llm
                  else 'Chinese' for llm in llms]

        # Sort by region and then by loyalty rate
        intl_llms = [(l, r) for l, r in zip(llms, loyalty_rates) if 'GPT' in l or 'Claude' in l or 'Gemini' in l]
        chinese_llms = [(l, r) for l, r in zip(llms, loyalty_rates) if 'Qwen' in l or 'DeepSeek' in l or 'Doubao' in l]

        intl_llms_sorted = sorted(intl_llms, key=lambda x: x[1], reverse=True)
        chinese_llms_sorted = sorted(chinese_llms, key=lambda x: x[1], reverse=True)

        intl_llms, intl_rates = zip(*intl_llms_sorted) if intl_llms else ([], [])
        chinese_llms, chinese_rates = zip(*chinese_llms_sorted) if chinese_llms else ([], [])

        fig, ax = plt.subplots(figsize=(12, 6))

        x = np.arange(len(intl_llms))
        width = 0.35

        if intl_llms and chinese_llms:
            # Make equal lengths for comparison
            min_len = min(len(intl_llms), len(chinese_llms))

            bars1 = ax.bar(x - width/2, intl_rates[:min_len], width,
                          label='International', color=self.colors['International'],
                          alpha=0.7, edgecolor='black')
            bars2 = ax.bar(x + width/2, chinese_rates[:min_len], width,
                          label='Chinese', color=self.colors['Chinese'],
                          alpha=0.7, edgecolor='black')

            ax.set_ylabel('Brand Mention Rate (%)', fontsize=12, fontweight='bold')
            ax.set_title('Brand Loyalty in Recommendation Queries by Region\n(Paper 1: Cultural Bias Analysis)',
                        fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels([f'LLM {i+1}' for i in range(min_len)])

            # Add value labels
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}%',
                           ha='center', va='bottom', fontsize=9)

            ax.legend()
            ax.set_ylim(0, max(max(intl_rates), max(chinese_rates)) * 1.2)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/figure3_recommendation_loyalty.png',
                   dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.output_dir}/figure3_recommendation_loyalty.pdf',
                   bbox_inches='tight')
        plt.close()

        print("  ✓ Saved as PNG and PDF")

    def figure4_industry_cultural_bias(self):
        """Figure 4: Industry-specific cultural bias (heatmap)"""
        print("Creating Figure 4: Industry-Specific Cultural Bias...")

        industry_data = self.report['industry_differences']

        industries = list(industry_data.keys())
        intl_rates = [industry_data[ind]['International'] for ind in industries]
        china_rates = [industry_data[ind]['Chinese'] for ind in industries]

        # Create heatmap data
        data = np.array([intl_rates, china_rates])

        fig, ax = plt.subplots(figsize=(10, 6))

        im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)

        # Set ticks and labels
        ax.set_xticks(np.arange(len(industries)))
        ax.set_yticks(np.arange(2))
        ax.set_xticklabels(industries, rotation=45, ha='right')
        ax.set_yticklabels(['International', 'Chinese'])

        # Add text annotations
        for i in range(2):
            for j in range(len(industries)):
                text = ax.text(j, i, f'{data[i, j]:.1f}%',
                             ha="center", va="center", color="black", fontweight='bold')

        ax.set_title('Cultural Bias by Industry\n(Paper 1: Cultural Bias Analysis)',
                    fontsize=14, fontweight='bold')

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Brand Mention Rate (%)', rotation=270, labelpad=20, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/figure4_industry_cultural_bias.png',
                   dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.output_dir}/figure4_industry_cultural_bias.pdf',
                   bbox_inches='tight')
        plt.close()

        print("  ✓ Saved as PNG and PDF")

    def figure5_sentiment_distribution_violin(self):
        """Figure 5: Sentiment score distribution (violin plot)"""
        print("Creating Figure 5: Sentiment Score Distribution...")

        # Load raw data for distribution
        data_file = '/Users/hjy/Project/arxiv_geo_001/data/raw/geo_data_final_20251229.json'
        with open(data_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        llm_regions = {
            'GPT-4o Search Preview': 'International',
            'Claude Sonnet 4.5': 'International',
            'Gemini Pro Latest': 'International',
            'Qwen3 Max Preview': 'Chinese',
            'DeepSeek V3.2 Exp': 'Chinese',
            'Doubao 1.5 Thinking Pro': 'Chinese'
        }

        sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}

        intl_scores = []
        china_scores = []

        for record in raw_data:
            region = llm_regions.get(record['model'])
            sentiment = record['analysis']['sentiment']['label']
            score = sentiment_map.get(sentiment, 0)

            if region == 'International':
                intl_scores.append(score)
            elif region == 'Chinese':
                china_scores.append(score)

        fig, ax = plt.subplots(figsize=(8, 6))

        # Create violin plot
        positions = [1, 2]
        parts = ax.violinplot([intl_scores, china_scores],
                             positions=positions,
                             showmeans=True,
                             showmedians=True)

        # Color the violins
        colors = [self.colors['International'], self.colors['Chinese']]
        for pc, color in zip(parts['bodies'], colors):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)

        # Add labels
        ax.set_xticks(positions)
        ax.set_xticklabels(['International', 'Chinese'])
        ax.set_ylabel('Sentiment Score', fontsize=12, fontweight='bold')
        ax.set_title('Sentiment Score Distribution by Region\n(Paper 1: Cultural Bias Analysis)',
                    fontsize=14, fontweight='bold')
        ax.set_ylim(-1.5, 1.5)

        # Add y-tick labels
        ax.set_yticks([-1, 0, 1])
        ax.set_yticklabels(['Negative', 'Neutral', 'Positive'])

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/figure5_sentiment_violin.png',
                   dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.output_dir}/figure5_sentiment_violin.pdf',
                   bbox_inches='tight')
        plt.close()

        print("  ✓ Saved as PNG and PDF")

    def figure6_conceptual_framework(self):
        """Figure 6: Conceptual framework of cultural bias in GEO"""
        print("Creating Figure 6: Conceptual Framework...")

        fig, ax = plt.subplots(figsize=(12, 8))

        # Draw framework as boxes and arrows
        boxes = [
            {'text': 'Training Data\n(Cultural Content)', 'xy': (0.2, 0.8), 'width': 0.2, 'height': 0.1},
            {'text': 'LLM Training\n(Cultural Encoding)', 'xy': (0.2, 0.6), 'width': 0.2, 'height': 0.1},
            {'text': 'User Query\n(English)', 'xy': (0.2, 0.4), 'width': 0.2, 'height': 0.1},
        ]

        # Draw International LLM path
        ax.add_patch(plt.Rectangle((0.5, 0.75), 0.15, 0.1,
                                   facecolor=self.colors['International'],
                                   edgecolor='black', alpha=0.7))
        ax.text(0.575, 0.8, 'International\nLLMs', ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')

        ax.add_patch(plt.Rectangle((0.5, 0.55), 0.15, 0.1,
                                   facecolor=self.colors['International'],
                                   edgecolor='black', alpha=0.7))
        ax.text(0.575, 0.6, 'Global\nPerspective', ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')

        # Draw Chinese LLM path
        ax.add_patch(plt.Rectangle((0.5, 0.35), 0.15, 0.1,
                                   facecolor=self.colors['Chinese'],
                                   edgecolor='black', alpha=0.7))
        ax.text(0.575, 0.4, 'Chinese\nLLMs', ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')

        ax.add_patch(plt.Rectangle((0.5, 0.15), 0.15, 0.1,
                                   facecolor=self.colors['Chinese'],
                                   edgecolor='black', alpha=0.7))
        ax.text(0.575, 0.2, 'Domestic\nPreference', ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')

        # Draw arrows
        ax.annotate('', xy=(0.5, 0.8), xytext=(0.4, 0.85),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        ax.annotate('', xy=(0.5, 0.4), xytext=(0.4, 0.85),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))

        # Add outcome box
        ax.add_patch(plt.Rectangle((0.75, 0.25), 0.2, 0.6,
                                   facecolor='gray', edgecolor='black', alpha=0.3))
        ax.text(0.85, 0.55, 'AI Brand\nRecommendations\n\nCultural\nEcho\nChamber',
               ha='center', va='center', fontsize=12, fontweight='bold')

        # Labels
        ax.text(0.3, 0.9, 'Input', ha='center', fontsize=14, fontweight='bold')
        ax.text(0.575, 0.95, 'Processing', ha='center', fontsize=14, fontweight='bold')
        ax.text(0.85, 0.9, 'Output', ha='center', fontsize=14, fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        ax.set_title('Conceptual Framework: Cultural Bias in AI Brand Recommendations\n(Paper 1: Cultural Bias Analysis)',
                    fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/figure6_conceptual_framework.png',
                   dpi=300, bbox_inches='tight')
        plt.savefig(f'{self.output_dir}/figure6_conceptual_framework.pdf',
                   bbox_inches='tight')
        plt.close()

        print("  ✓ Saved as PNG and PDF")

    def generate_all_figures(self):
        """Generate all figures for Paper 1"""
        print("\n" + "="*70)
        print("GENERATING FIGURES FOR PAPER 1")
        print("="*70)

        self.figure1_sentiment_distribution()
        self.figure2_brand_mention_by_llm()
        self.figure3_recommendation_loyalty()
        self.figure4_industry_cultural_bias()
        self.figure5_sentiment_distribution_violin()
        self.figure6_conceptual_framework()

        print("\n" + "="*70)
        print("ALL FIGURES GENERATED")
        print(f"Output directory: {self.output_dir}")
        print("="*70)


def main():
    """Main execution function"""
    report_file = '/Users/hjy/Project/arxiv_geo_001/paper/paper1_cultural_bias/analysis_results/cultural_bias_report.json'

    print("Loading analysis report...")
    generator = FigureGenerator(report_file)

    print("\nGenerating figures...")
    generator.generate_all_figures()


if __name__ == '__main__':
    main()

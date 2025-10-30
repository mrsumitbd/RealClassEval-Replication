"""
RQ4 Detailed Breakdowns for Discussion Points
Extracts:
1. Error distributions by dataset (ClassEval vs csn vs post_cut-off)
2. RAG error substitution patterns for significant models
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys


# Reuse the prepare_error_report function
def prepare_error_report(report_df):
    """Process raw test reports into error count matrix."""
    report_df = report_df.copy()

    # Filter out xfail
    report_df = report_df[report_df.markers.isnull()]

    # Keep fails only
    report_df = report_df[report_df['status'] == 'failed']

    if report_df.empty:
        return pd.DataFrame(columns=['snippet_id'])

    report_df['snippet_id'] = [module.split(".test_")[1] for module in report_df['module'].tolist()]

    report_df = report_df[['module', 'message', 'snippet_id']]

    report_df['error_types'] = [message.split(":")[0] if "Error:" in message else "Other"
                                for message in report_df.message.tolist()]

    report_df.drop(columns=['module', "message"], inplace=True)

    res_list = []
    standard_errors = [
        'AttributeError', 'TypeError', 'ValueError', 'NameError',
        'IndexError', 'KeyError', 'ZeroDivisionError', 'FileNotFoundError',
        'AssertionError', 'ImportError', 'RuntimeError', 'SyntaxError'
    ]

    # Replace non-standard errors with 'Other'
    report_df['error_types'] = report_df['error_types'].apply(
        lambda x: x if x in standard_errors else 'Other'
    )

    standard_errors.append("Other")

    for snippet in report_df.snippet_id.unique():
        snippet_list = [snippet]
        for error in standard_errors:
            snippet_list.append(
                report_df[(report_df['snippet_id'] == snippet) &
                          (report_df['error_types'] == error)].shape[0]
            )
        res_list.append(snippet_list)

    return pd.DataFrame(res_list, columns=['snippet_id'] + standard_errors)


class DetailedBreakdownAnalyzer:
    def __init__(self, base_path="../functional_correctness_test_folder"):
        self.base_path = Path(base_path)
        self.models = ['codestral', 'deepseek-ai', 'gpt-4.1', 'gpt-5',
                       'openai', 'meta-llama', 'qwen']
        self.datasets = ['ClassEval', 'csn', 'post_cut-off']
        self.docstring_conditions = ['full_docstr', 'partial_docstr', 'no_docstr']
        self.error_types = [
            'AttributeError', 'TypeError', 'ValueError', 'NameError',
            'IndexError', 'KeyError', 'ZeroDivisionError', 'FileNotFoundError',
            'AssertionError', 'ImportError', 'RuntimeError', 'SyntaxError', 'Other'
        ]

        print("=" * 80)
        print("RQ4: DETAILED BREAKDOWNS FOR DISCUSSION")
        print("=" * 80)

    def analyze_dataset_specific_distributions(self):
        """
        Analysis 1: Error distributions by dataset
        Shows which error types are more common in synthetic vs real-world
        """
        print("\n" + "=" * 80)
        print("ANALYSIS 1: ERROR DISTRIBUTIONS BY DATASET")
        print("=" * 80)

        dataset_errors = {}

        for dataset in self.datasets:
            dataset_errors[dataset] = {error: 0 for error in self.error_types}

            for model in self.models:
                for doc_cond in self.docstring_conditions:
                    report_path = self.base_path / dataset / model / f"{doc_cond}_reports" / "combined_test_report.csv"

                    if report_path.exists():
                        df = pd.read_csv(report_path)
                        error_df = prepare_error_report(df)

                        for error in self.error_types:
                            if error in error_df.columns:
                                dataset_errors[dataset][error] += error_df[error].sum()

        # Create comparison DataFrame
        comparison_df = pd.DataFrame(dataset_errors).T
        comparison_df['Total'] = comparison_df.sum(axis=1)

        # Calculate percentages
        comparison_pct = comparison_df.div(comparison_df['Total'], axis=0) * 100
        comparison_pct = comparison_pct.drop('Total', axis=1)

        print("\nError Type Distribution by Dataset (%):")
        print(comparison_pct.round(2).to_string())

        # Calculate differences
        print("\n" + "=" * 80)
        print("SYNTHETIC VS REAL-WORLD COMPARISON")
        print("=" * 80)

        # ClassEval vs Pre-Cutoff
        diff_pre = comparison_pct.loc['ClassEval'] - comparison_pct.loc['csn']
        diff_pre = diff_pre.sort_values(ascending=False)

        print("\nClassEval vs Pre-Cutoff (percentage point differences):")
        print("Positive = more common in ClassEval, Negative = more common in Pre-Cutoff")
        print(diff_pre.to_string())

        # ClassEval vs Post-Cutoff
        diff_post = comparison_pct.loc['ClassEval'] - comparison_pct.loc['post_cut-off']
        diff_post = diff_post.sort_values(ascending=False)

        print("\nClassEval vs Post-Cutoff (percentage point differences):")
        print("Positive = more common in ClassEval, Negative = more common in Post-Cutoff")
        print(diff_post.to_string())

        # Pre-Cutoff vs Post-Cutoff
        diff_temporal = comparison_pct.loc['csn'] - comparison_pct.loc['post_cut-off']
        diff_temporal = diff_temporal.sort_values(ascending=False)

        print("\nPre-Cutoff vs Post-Cutoff (percentage point differences):")
        print(diff_temporal.to_string())

        # Save results
        comparison_pct.to_csv('../results/rq4/dataset_error_distributions.csv')
        diff_pre.to_csv('../results/rq4/classeval_vs_precutoff_diff.csv')
        diff_post.to_csv('../results/rq4/classeval_vs_postcutoff_diff.csv')

        print("\n✓ Saved dataset_error_distributions.csv")
        print("✓ Saved classeval_vs_precutoff_diff.csv")
        print("✓ Saved classeval_vs_postcutoff_diff.csv")

        return comparison_pct, diff_pre, diff_post

    def analyze_rag_error_substitution(self):
        """
        Analysis 2: RAG error substitution for significant models with partial docstrings
        Shows which errors RAG reduces vs increases
        """
        print("\n" + "=" * 80)
        print("ANALYSIS 2: RAG ERROR SUBSTITUTION (Partial Docstrings)")
        print("=" * 80)

        # Models with significant RAG impact on partial docstrings
        significant_models = ['deepseek-ai', 'gpt-5', 'meta-llama']

        results = []

        for model in significant_models:
            print(f"\n{model.upper()}:")
            print("-" * 80)

            # Non-RAG errors
            non_rag_errors = {error: 0 for error in self.error_types}
            non_rag_path = self.base_path / 'post_cut-off' / model / 'partial_docstr_reports' / 'combined_test_report.csv'

            if non_rag_path.exists():
                df = pd.read_csv(non_rag_path)
                error_df = prepare_error_report(df)
                for error in self.error_types:
                    if error in error_df.columns:
                        non_rag_errors[error] = error_df[error].sum()

            # RAG errors
            rag_errors = {error: 0 for error in self.error_types}
            rag_path = self.base_path / 'post_cut-off' / 'rag' / model / 'partial_docstr_reports' / 'combined_test_report.csv'

            if rag_path.exists():
                df = pd.read_csv(rag_path)
                error_df = prepare_error_report(df)
                for error in self.error_types:
                    if error in error_df.columns:
                        rag_errors[error] = error_df[error].sum()

            # Calculate differences
            total_non_rag = sum(non_rag_errors.values())
            total_rag = sum(rag_errors.values())

            print(f"Total errors without RAG: {total_non_rag}")
            print(f"Total errors with RAG: {total_rag}")
            print(f"Net reduction: {total_non_rag - total_rag} errors ({(1 - total_rag / total_non_rag) * 100:.1f}%)")

            # Create comparison DataFrame
            comparison = pd.DataFrame({
                'Non-RAG_Count': pd.Series(non_rag_errors),
                'RAG_Count': pd.Series(rag_errors)
            })

            comparison['Absolute_Diff'] = comparison['RAG_Count'] - comparison['Non-RAG_Count']
            comparison['Percent_Change'] = ((comparison['RAG_Count'] - comparison['Non-RAG_Count']) /
                                            comparison['Non-RAG_Count'] * 100).replace([np.inf, -np.inf], 0)

            # Calculate percentage of total
            comparison['Non-RAG_Pct'] = (comparison['Non-RAG_Count'] / total_non_rag * 100).round(2)
            comparison['RAG_Pct'] = (comparison['RAG_Count'] / total_rag * 100).round(2)
            comparison['Pct_Point_Diff'] = comparison['RAG_Pct'] - comparison['Non-RAG_Pct']

            # Sort by absolute difference (most reduced first)
            comparison = comparison.sort_values('Absolute_Diff')

            print("\nError Type Changes (sorted by reduction):")
            print(comparison.to_string())

            # Identify patterns
            reduced = comparison[comparison['Absolute_Diff'] < -5]
            increased = comparison[comparison['Absolute_Diff'] > 5]

            if not reduced.empty:
                print(f"\n✓ Errors REDUCED by >5 instances:")
                for error, row in reduced.iterrows():
                    print(f"  - {error}: {int(row['Non-RAG_Count'])} → {int(row['RAG_Count'])} "
                          f"({row['Absolute_Diff']:.0f}, {row['Percent_Change']:.1f}%)")

            if not increased.empty:
                print(f"\n✗ Errors INCREASED by >5 instances:")
                for error, row in increased.iterrows():
                    print(f"  - {error}: {int(row['Non-RAG_Count'])} → {int(row['RAG_Count'])} "
                          f"(+{row['Absolute_Diff']:.0f}, +{row['Percent_Change']:.1f}%)")

            # Save individual model results
            comparison.to_csv(f'../results/rq4/rag_substitution_{model}.csv')
            print(f"\n✓ Saved rag_substitution_{model}.csv")

            results.append({
                'model': model,
                'comparison': comparison
            })

        # Aggregate analysis across all three models
        print("\n" + "=" * 80)
        print("AGGREGATE PATTERN ACROSS SIGNIFICANT MODELS")
        print("=" * 80)

        aggregate_non_rag = {error: 0 for error in self.error_types}
        aggregate_rag = {error: 0 for error in self.error_types}

        for result in results:
            comp = result['comparison']
            for error in self.error_types:
                aggregate_non_rag[error] += comp.loc[error, 'Non-RAG_Count']
                aggregate_rag[error] += comp.loc[error, 'RAG_Count']

        aggregate_df = pd.DataFrame({
            'Non-RAG_Count': pd.Series(aggregate_non_rag),
            'RAG_Count': pd.Series(aggregate_rag)
        })

        aggregate_df['Absolute_Diff'] = aggregate_df['RAG_Count'] - aggregate_df['Non-RAG_Count']
        total_agg_non_rag = aggregate_df['Non-RAG_Count'].sum()
        total_agg_rag = aggregate_df['RAG_Count'].sum()
        aggregate_df['Non-RAG_Pct'] = (aggregate_df['Non-RAG_Count'] / total_agg_non_rag * 100).round(2)
        aggregate_df['RAG_Pct'] = (aggregate_df['RAG_Count'] / total_agg_rag * 100).round(2)
        aggregate_df['Pct_Point_Diff'] = aggregate_df['RAG_Pct'] - aggregate_df['Non-RAG_Pct']

        aggregate_df = aggregate_df.sort_values('Absolute_Diff')

        print("\nAggregate Error Changes Across Deepseek-AI, GPT-5, Meta-Llama:")
        print(aggregate_df.to_string())

        aggregate_df.to_csv('../results/rq4/rag_substitution_aggregate.csv')
        print("\n✓ Saved rag_substitution_aggregate.csv")

        return results, aggregate_df

    def run_detailed_analysis(self):
        """Run both detailed analyses"""
        dist_pct, diff_pre, diff_post = self.analyze_dataset_specific_distributions()
        rag_results, rag_aggregate = self.analyze_rag_error_substitution()

        print("\n" + "=" * 80)
        print("DETAILED ANALYSIS COMPLETE")
        print("=" * 80)
        print("\nFiles generated:")
        print("1. dataset_error_distributions.csv")
        print("2. classeval_vs_precutoff_diff.csv")
        print("3. classeval_vs_postcutoff_diff.csv")
        print("4. rag_substitution_deepseek-ai.csv")
        print("5. rag_substitution_gpt-5.csv")
        print("6. rag_substitution_meta-llama.csv")
        print("7. rag_substitution_aggregate.csv")
        print("\nUse these for detailed discussion in RQ4 writeup!")


if __name__ == "__main__":
    analyzer = DetailedBreakdownAnalyzer(base_path="../functional_correctness_test_folder")
    analyzer.run_detailed_analysis()

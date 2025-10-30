"""
RQ4: Comprehensive Error Analysis
What are the most common errors in LLM-generated class-level code?

This script performs:
1. Overall error distribution analysis
2. Dataset-wise comparisons (ClassEval vs Pre-Cutoff vs Post-Cutoff)
3. Docstring impact on error patterns
4. RAG impact on error patterns
5. Model-specific error profiles
6. Power analysis for all chi-square tests
7. Qualitative error sampling for case studies
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, power_divergence
from statsmodels.stats.multitest import multipletests
from itertools import combinations
from scipy.stats import ncx2
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def prepare_error_report(report_df):
    """
    Process raw test reports into error count matrix.
    Reuses the exact function from the original script.
    """
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


def bootstrap_cramers_v_ci(contingency_table, n_bootstrap=1000, ci=0.95):
    """
    Calculate bootstrap confidence interval for Cramér's V.
    Handles zero cells in bootstrap samples gracefully.
    """
    # Flatten the contingency table to get original data structure
    row_totals = contingency_table.sum(axis=1)
    col_totals = contingency_table.sum(axis=0)
    n_total = contingency_table.sum().sum()

    # Create data representation for bootstrapping
    # Each row/col combination weighted by its frequency
    data_rows = []
    for i in range(len(row_totals)):
        for j in range(len(col_totals)):
            count = contingency_table.iloc[i, j] if isinstance(contingency_table, pd.DataFrame) else contingency_table[i, j]
            data_rows.extend([[i, j]] * int(count))

    data_array = np.array(data_rows)

    cramers_v_boots = []
    successful_boots = 0
    max_attempts = n_bootstrap * 3  # Try up to 3x the desired number

    for attempt in range(max_attempts):
        if successful_boots >= n_bootstrap:
            break

        # Resample with replacement
        boot_idx = np.random.choice(len(data_array), size=len(data_array), replace=True)
        boot_sample = data_array[boot_idx]

        # Create bootstrapped contingency table
        boot_table = np.zeros_like(contingency_table, dtype=float)
        for row, col in boot_sample:
            boot_table[row, col] += 1

        # Check if table is valid (no zero rows/columns that would cause issues)
        try:
            # Calculate Cramér's V
            chi2, _, _, expected = chi2_contingency(boot_table)

            # Additional check: ensure expected frequencies are reasonable
            if np.all(expected > 0):
                n = boot_table.sum()
                min_dim = min(boot_table.shape[0] - 1, boot_table.shape[1] - 1)
                cramers_v = np.sqrt(chi2 / (n * min_dim))
                cramers_v_boots.append(cramers_v)
                successful_boots += 1
        except (ValueError, Warning):
            # Skip this bootstrap sample if it causes issues
            continue

    # If we couldn't get enough successful bootstraps, return NaN
    if len(cramers_v_boots) < 100:  # Need at least 100 successful samples
        return np.nan, np.nan

    # Calculate confidence interval
    lower = np.percentile(cramers_v_boots, (1 - ci) / 2 * 100)
    upper = np.percentile(cramers_v_boots, (1 + ci) / 2 * 100)

    return lower, upper


def compute_effect_size(contingency_table):
    """
    Compute Cramér's V effect size with interpretation.
    """
    chi2, _, _, _ = chi2_contingency(contingency_table)
    n = contingency_table.sum().sum()
    min_dim = min(contingency_table.shape[0] - 1, contingency_table.shape[1] - 1)

    cramers_v = np.sqrt(chi2 / (n * min_dim))

    # Interpretation based on Cohen (1988)
    if cramers_v < 0.1:
        interpretation = "Negligible"
    elif cramers_v < 0.3:
        interpretation = "Small"
    elif cramers_v < 0.5:
        interpretation = "Medium"
    else:
        interpretation = "Large"

    return cramers_v, interpretation


def compute_chi_square_power(contingency_table, alpha=0.05):
    """
    Compute statistical power for chi-square test.
    Uses effect size (w) from observed data.
    """
    chi2, _, dof, _ = chi2_contingency(contingency_table)
    n = contingency_table.sum().sum()

    # Effect size w = sqrt(chi2 / n)
    w = np.sqrt(chi2 / n)

    # Non-centrality parameter
    ncp = chi2

    # Critical value
    from scipy.stats import chi2 as chi2_dist
    critical_value = chi2_dist.ppf(1 - alpha, dof)

    # Power = P(Chi2 > critical_value | ncp)
    power = 1 - ncx2.cdf(critical_value, dof, ncp)

    return power, w


class RQ4ErrorAnalyzer:
    """
    Comprehensive error analysis for RQ4.
    """

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

        # Storage for loaded data
        self.data = {}
        self.results = {}

        print("=" * 80)
        print("RQ4: COMPREHENSIVE ERROR ANALYSIS")
        print("=" * 80)
        print(f"\nModels: {', '.join(self.models)}")
        print(f"Datasets: {', '.join(self.datasets)}")
        print(f"Docstring conditions: {', '.join(self.docstring_conditions)}")
        print(f"Error types tracked: {len(self.error_types)}")

    def load_all_data(self):
        """
        Load all test reports systematically.
        """
        print("\n" + "=" * 80)
        print("LOADING DATA")
        print("=" * 80)

        for model in self.models:
            self.data[model] = {}
            for dataset in self.datasets:
                self.data[model][dataset] = {}

                # Non-RAG conditions
                for doc_cond in self.docstring_conditions:
                    report_path = self.base_path / dataset / model / f"{doc_cond}_reports" / "combined_test_report.csv"

                    if report_path.exists():
                        df = pd.read_csv(report_path)
                        error_df = prepare_error_report(df)
                        self.data[model][dataset][doc_cond] = error_df
                        print(f"✓ Loaded {model}/{dataset}/{doc_cond}: {len(error_df)} failed snippets")
                    else:
                        print(f"✗ Missing: {report_path}")
                        self.data[model][dataset][doc_cond] = pd.DataFrame(columns=['snippet_id'] + self.error_types)

                # RAG conditions (only for post_cut-off)
                if dataset == 'post_cut-off':
                    for doc_cond in self.docstring_conditions:
                        rag_path = self.base_path / dataset / "rag" / model / f"{doc_cond}_reports" / "combined_test_report.csv"

                        if rag_path.exists():
                            df = pd.read_csv(rag_path)
                            error_df = prepare_error_report(df)
                            self.data[model][dataset][f"rag_{doc_cond}"] = error_df
                            print(f"✓ Loaded {model}/{dataset}/rag_{doc_cond}: {len(error_df)} failed snippets")
                        else:
                            print(f"✗ Missing: {rag_path}")
                            self.data[model][dataset][f"rag_{doc_cond}"] = pd.DataFrame(columns=['snippet_id'] + self.error_types)

        print("\nData loading complete!")

    def overall_error_distribution(self):
        """
        Analysis 1: Overall error distribution across all conditions.
        Chi-square goodness-of-fit test against uniform distribution.
        """
        print("\n" + "=" * 80)
        print("ANALYSIS 1: OVERALL ERROR DISTRIBUTION")
        print("=" * 80)

        # Aggregate all errors
        total_errors = {error: 0 for error in self.error_types}

        for model in self.models:
            for dataset in self.datasets:
                for condition in self.data[model][dataset].keys():
                    df = self.data[model][dataset][condition]
                    for error in self.error_types:
                        if error in df.columns:
                            total_errors[error] += df[error].sum()

        # Create summary DataFrame
        error_df = pd.DataFrame({
            'Error Type': list(total_errors.keys()),
            'Count': list(total_errors.values())
        })
        error_df['Percentage'] = (error_df['Count'] / error_df['Count'].sum() * 100).round(2)
        error_df = error_df.sort_values('Count', ascending=False).reset_index(drop=True)

        print("\nError Type Distribution (All Conditions):")
        print(error_df.to_string(index=False))

        # Chi-square goodness-of-fit test (against uniform distribution)
        observed = error_df['Count'].values
        expected = np.full(len(observed), observed.sum() / len(observed))
        chi2, p_value = power_divergence(observed, expected, lambda_='pearson')

        print(f"\nChi-square goodness-of-fit test (vs. uniform distribution):")
        print(f"  χ² = {chi2:.2f}")
        print(f"  p-value = {p_value:.4e}")
        print(f"  Result: {'Significantly non-uniform' if p_value < 0.05 else 'Not significantly different from uniform'}")

        # Top errors
        top_5 = error_df.head(5)
        coverage = top_5['Percentage'].sum()
        print(f"\nTop 5 errors cover {coverage:.1f}% of all failures:")
        for idx, row in top_5.iterrows():
            print(f"  {idx+1}. {row['Error Type']}: {row['Count']} ({row['Percentage']:.1f}%)")

        self.results['overall_distribution'] = error_df

        # Generate LaTeX table
        latex_table = self._generate_latex_table_overall(error_df)
        self.results['overall_distribution_latex'] = latex_table

        return error_df

    def dataset_comparison(self):
        """
        Analysis 2: Compare error distributions across datasets (ClassEval vs Pre-Cutoff vs Post-Cutoff).
        Pairwise chi-square tests with FDR correction.
        """
        print("\n" + "=" * 80)
        print("ANALYSIS 2: DATASET-WISE ERROR DISTRIBUTION COMPARISON")
        print("=" * 80)

        results_list = []

        # For each model, compare datasets pairwise
        for model in self.models:
            print(f"\n{model.upper()}:")

            # Aggregate errors by dataset (across all docstring conditions)
            dataset_errors = {}
            for dataset in self.datasets:
                dataset_errors[dataset] = {error: 0 for error in self.error_types}
                for condition in self.docstring_conditions:
                    if condition in self.data[model][dataset]:
                        df = self.data[model][dataset][condition]
                        for error in self.error_types:
                            if error in df.columns:
                                dataset_errors[dataset][error] += df[error].sum()

            # Pairwise comparisons
            pairs = list(combinations(self.datasets, 2))
            for ds1, ds2 in pairs:
                # Create contingency table
                errors_ds1 = [dataset_errors[ds1][e] for e in self.error_types]
                errors_ds2 = [dataset_errors[ds2][e] for e in self.error_types]

                contingency = pd.DataFrame({
                    ds1: errors_ds1,
                    ds2: errors_ds2
                }, index=self.error_types)

                # Remove error types with zero counts in both
                contingency = contingency[(contingency.sum(axis=1) > 0)]

                if contingency.empty or contingency.shape[0] < 2:
                    print(f"  {ds1} vs {ds2}: Insufficient data")
                    continue

                # Chi-square test
                chi2, p_value, dof, expected = chi2_contingency(contingency)

                # Effect size
                cramers_v, effect_interp = compute_effect_size(contingency)

                # Bootstrap CI for Cramér's V
                ci_lower, ci_upper = bootstrap_cramers_v_ci(contingency, n_bootstrap=1000)

                # Power
                power, w = compute_chi_square_power(contingency)

                print(f"  {ds1} vs {ds2}:")
                print(f"    χ² = {chi2:.2f}, p = {p_value:.4e}")
                if not np.isnan(ci_lower):
                    print(f"    Cramér's V = {cramers_v:.3f} ({effect_interp}), 95% CI [{ci_lower:.3f}, {ci_upper:.3f}]")
                else:
                    print(f"    Cramér's V = {cramers_v:.3f} ({effect_interp}), 95% CI [unavailable]")
                print(f"    Power = {power:.3f}")

                results_list.append({
                    'Model': model,
                    'Comparison': f"{ds1} vs {ds2}",
                    'Chi2': chi2,
                    'p_value': p_value,
                    'Cramers_V': cramers_v,
                    'Effect_Size': effect_interp,
                    'CI_Lower': ci_lower if not np.isnan(ci_lower) else None,
                    'CI_Upper': ci_upper if not np.isnan(ci_upper) else None,
                    'Power': power
                })

        # FDR correction (21 tests: 3 comparisons × 7 models)
        results_df = pd.DataFrame(results_list)
        if not results_df.empty:
            _, p_adjusted, _, _ = multipletests(results_df['p_value'], alpha=0.05, method='fdr_bh')
            results_df['p_FDR'] = p_adjusted
            results_df['Significant'] = results_df['p_FDR'] < 0.05

            print("\n" + "=" * 80)
            print("DATASET COMPARISON SUMMARY (with FDR correction)")
            print("=" * 80)
            print(results_df[['Model', 'Comparison', 'Chi2', 'p_value', 'p_FDR',
                            'Cramers_V', 'Effect_Size', 'Power', 'Significant']].to_string(index=False))

            sig_count = results_df['Significant'].sum()
            print(f"\nSignificant differences after FDR correction: {sig_count}/{len(results_df)}")

            self.results['dataset_comparison'] = results_df

            # Generate LaTeX table
            latex_table = self._generate_latex_table_dataset(results_df)
            self.results['dataset_comparison_latex'] = latex_table

        return results_df

    def docstring_impact_on_errors(self):
        """
        Analysis 3: Impact of docstrings on error patterns.
        Separate analysis for Pre-Cutoff and Post-Cutoff (following RQ2 approach).
        """
        print("\n" + "=" * 80)
        print("ANALYSIS 3: DOCSTRING IMPACT ON ERROR PATTERNS")
        print("=" * 80)

        results_list = []

        for dataset in ['csn', 'post_cut-off']:
            print(f"\n{dataset.upper()} Dataset:")

            for model in self.models:
                print(f"\n  {model}:")

                # Aggregate errors by docstring condition
                doc_errors = {}
                for doc_cond in self.docstring_conditions:
                    doc_errors[doc_cond] = {error: 0 for error in self.error_types}
                    if doc_cond in self.data[model][dataset]:
                        df = self.data[model][dataset][doc_cond]
                        for error in self.error_types:
                            if error in df.columns:
                                doc_errors[doc_cond][error] += df[error].sum()

                # Pairwise comparisons
                pairs = [('full_docstr', 'partial_docstr'), ('full_docstr', 'no_docstr')]

                for doc1, doc2 in pairs:
                    errors_doc1 = [doc_errors[doc1][e] for e in self.error_types]
                    errors_doc2 = [doc_errors[doc2][e] for e in self.error_types]

                    contingency = pd.DataFrame({
                        doc1: errors_doc1,
                        doc2: errors_doc2
                    }, index=self.error_types)

                    # Remove zero rows
                    contingency = contingency[(contingency.sum(axis=1) > 0)]

                    if contingency.empty or contingency.shape[0] < 2:
                        print(f"    {doc1} vs {doc2}: Insufficient data")
                        continue

                    chi2, p_value, dof, expected = chi2_contingency(contingency)
                    cramers_v, effect_interp = compute_effect_size(contingency)
                    ci_lower, ci_upper = bootstrap_cramers_v_ci(contingency)
                    power, w = compute_chi_square_power(contingency)

                    print(f"    {doc1} vs {doc2}:")
                    if not np.isnan(ci_lower):
                        print(f"      χ² = {chi2:.2f}, p = {p_value:.4e}, Cramér's V = {cramers_v:.3f} ({effect_interp}), CI [{ci_lower:.3f}, {ci_upper:.3f}]")
                    else:
                        print(f"      χ² = {chi2:.2f}, p = {p_value:.4e}, Cramér's V = {cramers_v:.3f} ({effect_interp})")

                    results_list.append({
                        'Dataset': dataset,
                        'Model': model,
                        'Comparison': f"{doc1} vs {doc2}",
                        'Chi2': chi2,
                        'p_value': p_value,
                        'Cramers_V': cramers_v,
                        'Effect_Size': effect_interp,
                        'CI_Lower': ci_lower if not np.isnan(ci_lower) else None,
                        'CI_Upper': ci_upper if not np.isnan(ci_upper) else None,
                        'Power': power
                    })

        results_df = pd.DataFrame(results_list)

        if not results_df.empty:
            # Per-dataset FDR correction (following RQ2 approach)
            for dataset in ['csn', 'post_cut-off']:
                dataset_mask = results_df['Dataset'] == dataset
                dataset_pvals = results_df.loc[dataset_mask, 'p_value']

                if len(dataset_pvals) > 0:
                    _, p_adjusted, _, _ = multipletests(dataset_pvals, alpha=0.05, method='fdr_bh')
                    results_df.loc[dataset_mask, 'p_FDR'] = p_adjusted

            results_df['Significant'] = results_df['p_FDR'] < 0.05

            print("\n" + "=" * 80)
            print("DOCSTRING IMPACT SUMMARY (per-dataset FDR correction)")
            print("=" * 80)
            print(results_df[['Dataset', 'Model', 'Comparison', 'Chi2', 'p_value', 'p_FDR',
                            'Cramers_V', 'Effect_Size', 'Power', 'Significant']].to_string(index=False))

            # Summary by dataset
            for dataset in ['csn', 'post_cut-off']:
                dataset_results = results_df[results_df['Dataset'] == dataset]
                sig_count = dataset_results['Significant'].sum()
                print(f"\n{dataset}: {sig_count}/{len(dataset_results)} significant differences")

            self.results['docstring_impact'] = results_df

            # Generate LaTeX table
            latex_table = self._generate_latex_table_docstring(results_df)
            self.results['docstring_impact_latex'] = latex_table

        return results_df

    def rag_impact_on_errors(self):
        """
        Analysis 4: Impact of RAG on error patterns (Post-Cutoff only).
        Per-docstring-condition FDR correction (following RQ3 approach).
        """
        print("\n" + "=" * 80)
        print("ANALYSIS 4: RAG IMPACT ON ERROR PATTERNS (Post-Cutoff)")
        print("=" * 80)

        results_list = []

        for doc_cond in self.docstring_conditions:
            print(f"\n{doc_cond.upper()}:")

            for model in self.models:
                # Get non-RAG and RAG error distributions
                non_rag_errors = {error: 0 for error in self.error_types}
                rag_errors = {error: 0 for error in self.error_types}

                if doc_cond in self.data[model]['post_cut-off']:
                    df = self.data[model]['post_cut-off'][doc_cond]
                    for error in self.error_types:
                        if error in df.columns:
                            non_rag_errors[error] = df[error].sum()

                if f"rag_{doc_cond}" in self.data[model]['post_cut-off']:
                    df = self.data[model]['post_cut-off'][f"rag_{doc_cond}"]
                    for error in self.error_types:
                        if error in df.columns:
                            rag_errors[error] = df[error].sum()

                # Create contingency table
                errors_non_rag = [non_rag_errors[e] for e in self.error_types]
                errors_rag = [rag_errors[e] for e in self.error_types]

                contingency = pd.DataFrame({
                    'Non-RAG': errors_non_rag,
                    'RAG': errors_rag
                }, index=self.error_types)

                # Remove zero rows
                contingency = contingency[(contingency.sum(axis=1) > 0)]

                if contingency.empty or contingency.shape[0] < 2:
                    print(f"  {model}: Insufficient data")
                    continue

                chi2, p_value, dof, expected = chi2_contingency(contingency)
                cramers_v, effect_interp = compute_effect_size(contingency)
                ci_lower, ci_upper = bootstrap_cramers_v_ci(contingency)
                power, w = compute_chi_square_power(contingency)

                print(f"  {model}:")
                if not np.isnan(ci_lower):
                    print(f"    χ² = {chi2:.2f}, p = {p_value:.4e}, Cramér's V = {cramers_v:.3f} ({effect_interp}), CI [{ci_lower:.3f}, {ci_upper:.3f}]")
                else:
                    print(f"    χ² = {chi2:.2f}, p = {p_value:.4e}, Cramér's V = {cramers_v:.3f} ({effect_interp})")

                results_list.append({
                    'Docstring_Condition': doc_cond,
                    'Model': model,
                    'Chi2': chi2,
                    'p_value': p_value,
                    'Cramers_V': cramers_v,
                    'Effect_Size': effect_interp,
                    'CI_Lower': ci_lower if not np.isnan(ci_lower) else None,
                    'CI_Upper': ci_upper if not np.isnan(ci_upper) else None,
                    'Power': power
                })

        results_df = pd.DataFrame(results_list)

        if not results_df.empty:
            # Per-docstring-condition FDR correction (following RQ3 approach)
            for doc_cond in self.docstring_conditions:
                cond_mask = results_df['Docstring_Condition'] == doc_cond
                cond_pvals = results_df.loc[cond_mask, 'p_value']

                if len(cond_pvals) > 0:
                    _, p_adjusted, _, _ = multipletests(cond_pvals, alpha=0.05, method='fdr_bh')
                    results_df.loc[cond_mask, 'p_FDR'] = p_adjusted

            results_df['Significant'] = results_df['p_FDR'] < 0.05

            print("\n" + "=" * 80)
            print("RAG IMPACT SUMMARY (per-condition FDR correction)")
            print("=" * 80)
            print(results_df[['Docstring_Condition', 'Model', 'Chi2', 'p_value', 'p_FDR',
                            'Cramers_V', 'Effect_Size', 'Power', 'Significant']].to_string(index=False))

            # Summary by docstring condition
            for doc_cond in self.docstring_conditions:
                cond_results = results_df[results_df['Docstring_Condition'] == doc_cond]
                sig_count = cond_results['Significant'].sum()
                print(f"\n{doc_cond}: {sig_count}/{len(cond_results)} significant differences")

            self.results['rag_impact'] = results_df

            # Generate LaTeX table
            latex_table = self._generate_latex_table_rag(results_df)
            self.results['rag_impact_latex'] = latex_table

        return results_df

    def model_specific_error_profiles(self):
        """
        Analysis 5: Model-specific error profiles.
        Compare error distributions across models.
        """
        print("\n" + "=" * 80)
        print("ANALYSIS 5: MODEL-SPECIFIC ERROR PROFILES")
        print("=" * 80)

        # Aggregate errors by model (across all datasets and conditions)
        model_errors = {}
        for model in self.models:
            model_errors[model] = {error: 0 for error in self.error_types}
            for dataset in self.datasets:
                for condition in self.data[model][dataset].keys():
                    df = self.data[model][dataset][condition]
                    for error in self.error_types:
                        if error in df.columns:
                            model_errors[model][error] += df[error].sum()

        # Create profile matrix
        profile_df = pd.DataFrame(model_errors).T
        profile_df['Total'] = profile_df.sum(axis=1)

        # Calculate percentages
        profile_pct = profile_df.div(profile_df['Total'], axis=0) * 100
        profile_pct = profile_pct.drop('Total', axis=1)

        print("\nError Type Distribution by Model (%):")
        print(profile_pct.round(1).to_string())

        # Find most common error for each model
        print("\nMost Common Error by Model:")
        for model in self.models:
            top_error = profile_pct.loc[model].idxmax()
            top_pct = profile_pct.loc[model, top_error]
            print(f"  {model}: {top_error} ({top_pct:.1f}%)")

        # Pairwise model comparisons (sample: top 3 models by total errors)
        top_models = profile_df.nlargest(3, 'Total').index.tolist()

        print(f"\nPairwise comparisons for top 3 models: {', '.join(top_models)}")

        results_list = []
        pairs = list(combinations(top_models, 2))

        for m1, m2 in pairs:
            errors_m1 = [model_errors[m1][e] for e in self.error_types]
            errors_m2 = [model_errors[m2][e] for e in self.error_types]

            contingency = pd.DataFrame({
                m1: errors_m1,
                m2: errors_m2
            }, index=self.error_types)

            contingency = contingency[(contingency.sum(axis=1) > 0)]

            if contingency.empty or contingency.shape[0] < 2:
                continue

            chi2, p_value, dof, expected = chi2_contingency(contingency)
            cramers_v, effect_interp = compute_effect_size(contingency)
            power, w = compute_chi_square_power(contingency)

            print(f"\n  {m1} vs {m2}:")
            print(f"    χ² = {chi2:.2f}, p = {p_value:.4e}")
            print(f"    Cramér's V = {cramers_v:.3f} ({effect_interp})")

            results_list.append({
                'Comparison': f"{m1} vs {m2}",
                'Chi2': chi2,
                'p_value': p_value,
                'Cramers_V': cramers_v,
                'Effect_Size': effect_interp,
                'Power': power
            })

        if results_list:
            results_df = pd.DataFrame(results_list)
            _, p_adjusted, _, _ = multipletests(results_df['p_value'], alpha=0.05, method='fdr_bh')
            results_df['p_FDR'] = p_adjusted
            results_df['Significant'] = results_df['p_FDR'] < 0.05

            print("\nModel comparison results (with FDR correction):")
            print(results_df.to_string(index=False))

        self.results['model_profiles'] = profile_pct
        self.results['model_profile_latex'] = self._generate_latex_table_model_profile(profile_pct)

        return profile_pct

    def generate_qualitative_sample(self, n_per_error=5, output_dir="qualitative_samples"):
        """
        Generate random samples of each error type for qualitative analysis.
        """
        print("\n" + "=" * 80)
        print("GENERATING QUALITATIVE SAMPLES")
        print("=" * 80)

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Get top 5 errors from overall distribution
        overall_dist = self.results.get('overall_distribution')
        if overall_dist is None:
            print("Run overall_error_distribution() first!")
            return

        top_errors = overall_dist.head(7)['Error Type'].tolist()

        print(f"\nSampling {n_per_error} instances for each of top {len(top_errors)} error types...")

        samples = {error: [] for error in top_errors}

        # Collect all instances
        for model in self.models:
            for dataset in self.datasets:
                for condition in self.data[model][dataset].keys():
                    df = self.data[model][dataset][condition]

                    for error in top_errors:
                        if error not in df.columns:
                            continue

                        # Get snippets with this error
                        error_snippets = df[df[error] > 0]['snippet_id'].tolist()

                        for snippet_id in error_snippets:
                            samples[error].append({
                                'model': model,
                                'dataset': dataset,
                                'condition': condition,
                                'snippet_id': snippet_id,
                                'error_count': df[df['snippet_id'] == snippet_id][error].values[0]
                            })

        # Random sample and save
        for error in top_errors:
            if len(samples[error]) > 0:
                sampled = np.random.choice(
                    len(samples[error]),
                    size=min(n_per_error, len(samples[error])),
                    replace=False
                )

                sample_list = [samples[error][i] for i in sampled]
                sample_df = pd.DataFrame(sample_list)

                output_file = output_path / f"{error}_samples.csv"
                sample_df.to_csv(output_file, index=False)

                print(f"  {error}: {len(sample_df)} samples saved to {output_file}")

        print(f"\nQualitative samples saved to {output_dir}/")
        print("Use these for manual inspection and case study analysis.")

    def _generate_latex_table_overall(self, df):
        """Generate LaTeX table for overall error distribution."""
        latex = "\\begin{table}[t]\n\\centering\n"
        latex += "\\caption{Overall error type distribution across all conditions.}\n"
        latex += "\\label{tab:rq4_overall}\n"
        latex += "\\resizebox{\\columnwidth}{!}{\n"
        latex += "\\begin{tabular}{lcc}\n"
        latex += "\\toprule\n"
        latex += "\\textbf{Error Type} & \\textbf{Count} & \\textbf{Percentage (\\%)} \\\\\n"
        latex += "\\midrule\n"

        for idx, row in df.head(10).iterrows():
            latex += f"{row['Error Type']} & {int(row['Count'])} & {row['Percentage']:.2f} \\\\\n"

        latex += "\\bottomrule\n"
        latex += "\\end{tabular}}\n"
        latex += "\\end{table}\n"

        return latex

    def _generate_latex_table_dataset(self, df):
        """Generate LaTeX table for dataset comparison."""
        latex = "\\begin{table*}[t]\n\\centering\n"
        latex += "\\caption{Dataset-wise error distribution comparison with FDR correction.}\n"
        latex += "\\label{tab:rq4_dataset}\n"
        latex += "\\resizebox{\\textwidth}{!}{\n"
        latex += "\\begin{tabular}{llcccccc}\n"
        latex += "\\toprule\n"
        latex += "\\textbf{Model} & \\textbf{Comparison} & \\textbf{$\\chi^2$} & "
        latex += "\\textbf{p-value} & \\textbf{p\\textsubscript{FDR}} & "
        latex += "\\textbf{Cramér's V} & \\textbf{Effect Size} & \\textbf{Power} \\\\\n"
        latex += "\\midrule\n"

        for idx, row in df.iterrows():
            sig_marker = "\\textbf{" if row['Significant'] else ""
            sig_marker_end = "}" if row['Significant'] else ""

            latex += f"{row['Model']} & {row['Comparison']} & {row['Chi2']:.2f} & "
            latex += f"{sig_marker}{row['p_value']:.2e}{sig_marker_end} & "
            latex += f"{sig_marker}{row['p_FDR']:.2e}{sig_marker_end} & "
            latex += f"{row['Cramers_V']:.3f} & {row['Effect_Size']} & {row['Power']:.3f} \\\\\n"

        latex += "\\bottomrule\n"
        latex += "\\end{tabular}}\n"
        latex += "\\end{table*}\n"

        return latex

    def _generate_latex_table_docstring(self, df):
        """Generate LaTeX table for docstring impact."""
        latex = "\\begin{table*}[t]\n\\centering\n"
        latex += "\\caption{Docstring impact on error patterns with per-dataset FDR correction.}\n"
        latex += "\\label{tab:rq4_docstring}\n"
        latex += "\\resizebox{\\textwidth}{!}{\n"
        latex += "\\begin{tabular}{lllcccccc}\n"
        latex += "\\toprule\n"
        latex += "\\textbf{Dataset} & \\textbf{Model} & \\textbf{Comparison} & "
        latex += "\\textbf{$\\chi^2$} & \\textbf{p-value} & \\textbf{p\\textsubscript{FDR}} & "
        latex += "\\textbf{Cramér's V} & \\textbf{Effect} & \\textbf{Power} \\\\\n"
        latex += "\\midrule\n"

        for idx, row in df.iterrows():
            sig_marker = "\\textbf{" if row['Significant'] else ""
            sig_marker_end = "}" if row['Significant'] else ""

            latex += f"{row['Dataset']} & {row['Model']} & {row['Comparison']} & "
            latex += f"{row['Chi2']:.2f} & "
            latex += f"{sig_marker}{row['p_value']:.2e}{sig_marker_end} & "
            latex += f"{sig_marker}{row['p_FDR']:.2e}{sig_marker_end} & "
            latex += f"{row['Cramers_V']:.3f} & {row['Effect_Size'][:3]} & {row['Power']:.3f} \\\\\n"

        latex += "\\bottomrule\n"
        latex += "\\end{tabular}}\n"
        latex += "\\end{table*}\n"

        return latex

    def _generate_latex_table_rag(self, df):
        """Generate LaTeX table for RAG impact."""
        latex = "\\begin{table*}[t]\n\\centering\n"
        latex += "\\caption{RAG impact on error patterns with per-condition FDR correction.}\n"
        latex += "\\label{tab:rq4_rag}\n"
        latex += "\\resizebox{\\textwidth}{!}{\n"
        latex += "\\begin{tabular}{llcccccc}\n"
        latex += "\\toprule\n"
        latex += "\\textbf{Docstring} & \\textbf{Model} & \\textbf{$\\chi^2$} & "
        latex += "\\textbf{p-value} & \\textbf{p\\textsubscript{FDR}} & "
        latex += "\\textbf{Cramér's V} & \\textbf{Effect} & \\textbf{Power} \\\\\n"
        latex += "\\midrule\n"

        for idx, row in df.iterrows():
            sig_marker = "\\textbf{" if row['Significant'] else ""
            sig_marker_end = "}" if row['Significant'] else ""

            latex += f"{row['Docstring_Condition']} & {row['Model']} & "
            latex += f"{row['Chi2']:.2f} & "
            latex += f"{sig_marker}{row['p_value']:.2e}{sig_marker_end} & "
            latex += f"{sig_marker}{row['p_FDR']:.2e}{sig_marker_end} & "
            latex += f"{row['Cramers_V']:.3f} & {row['Effect_Size'][:3]} & {row['Power']:.3f} \\\\\n"

        latex += "\\bottomrule\n"
        latex += "\\end{tabular}}\n"
        latex += "\\end{table*}\n"

        return latex

    def _generate_latex_table_model_profile(self, df):
        """Generate LaTeX table for model profiles."""
        # Select top 7 error types by frequency
        top_errors = df.sum().nlargest(7).index.tolist()

        latex = "\\begin{table*}[t]\n\\centering\n"
        latex += "\\caption{Model-specific error profiles (\\% of total errors per model).}\n"
        latex += "\\label{tab:rq4_model_profile}\n"
        latex += "\\resizebox{\\textwidth}{!}{\n"
        latex += "\\begin{tabular}{l" + "c" * len(top_errors) + "}\n"
        latex += "\\toprule\n"
        latex += "\\textbf{Model} & " + " & ".join([f"\\textbf{{{e}}}" for e in top_errors]) + " \\\\\n"
        latex += "\\midrule\n"

        for model in self.models:
            latex += f"{model}"
            for error in top_errors:
                latex += f" & {df.loc[model, error]:.1f}"
            latex += " \\\\\n"

        latex += "\\bottomrule\n"
        latex += "\\end{tabular}}\n"
        latex += "\\end{table*}\n"

        return latex

    def save_all_results(self, output_dir="../results/rq4"):
        """
        Save all results to files.
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\n" + "=" * 80)
        print("SAVING RESULTS")
        print("=" * 80)

        # Save DataFrames
        for key, value in self.results.items():
            if isinstance(value, pd.DataFrame):
                csv_path = output_path / f"{key}.csv"
                value.to_csv(csv_path, index=False)
                print(f"✓ Saved {csv_path}")

        # # Save LaTeX tables
        # latex_path = output_path / "latex_tables.tex"
        # with open(latex_path, 'w') as f:
        #     f.write("% RQ4 LaTeX Tables\n\n")
        #     for key, value in self.results.items():
        #         if key.endswith('_latex'):
        #             f.write(f"% {key}\n")
        #             f.write(value)
        #             f.write("\n\n")
        #
        # print(f"✓ Saved all LaTeX tables to {latex_path}")

        print(f"\nAll results saved to {output_dir}/")

    def run_complete_analysis(self):
        """
        Run all analyses in sequence.
        """
        self.load_all_data()
        self.overall_error_distribution()
        self.dataset_comparison()
        self.docstring_impact_on_errors()
        self.rag_impact_on_errors()
        self.model_specific_error_profiles()
        self.generate_qualitative_sample(n_per_error=10)
        self.save_all_results()

        print("\n" + "=" * 80)
        print("RQ4 ANALYSIS COMPLETE")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Review results in rq4_results/ directory")
        print("2. Examine qualitative samples in qualitative_samples/ directory")
        print("3. Use LaTeX tables in your writeup")
        print("4. Conduct manual code inspection for case studies")


if __name__ == "__main__":
    # Initialize analyzer
    analyzer = RQ4ErrorAnalyzer(base_path="../functional_correctness_test_folder")

    # Run complete analysis
    analyzer.run_complete_analysis()

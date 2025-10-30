import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestPower
import os

# Define model names: folder names (for file access) and display names (for output)
model_mapping = {
    'codestral': 'Codestral',
    'deepseek-ai': 'Deepseek-V3',
    'gpt-4.1': 'GPT-4.1',
    'gpt-5': 'GPT-5',
    'openai': 'GPT-OSS',
    'meta-llama': 'Llama 4 Maverick',
    'Qwen': 'Qwen Coder 2.5'
}
models = list(model_mapping.keys())  # Folder names
display_order = list(model_mapping.values())  # Display names in RQ1 order
docstr_types = ['full_docstr', 'partial_docstr', 'no_docstr']


# Function to compute Cliff's Delta with bootstrap CI
def cliffs_delta(x, y, n_boot=1000):
    """
    Compute Cliff's Delta effect size with bootstrap confidence intervals.

    Parameters:
    -----------
    x, y : array-like
        Two samples to compare
    n_boot : int
        Number of bootstrap iterations

    Returns:
    --------
    delta : float
        Cliff's Delta value
    magnitude : str
        Effect size magnitude category
    ci : list
        95% confidence interval [lower, upper]
    """
    x = np.array(x)
    y = np.array(y)
    n = len(x)

    # Compute Cliff's Delta
    less = greater = 0
    for i in range(n):
        for j in range(n):
            if x[i] > y[j]:
                greater += 1
            elif x[i] < y[j]:
                less += 1
    delta = (greater - less) / (n * n)

    # Bootstrap confidence interval
    boots = []
    for _ in range(n_boot):
        indices = np.random.randint(0, n, n)
        x_boot = x[indices]
        y_boot = y[indices]
        less_boot = greater_boot = 0
        for i in range(n):
            for j in range(n):
                if x_boot[i] > y_boot[j]:
                    greater_boot += 1
                elif x_boot[i] < y_boot[j]:
                    less_boot += 1
        boots.append((greater_boot - less_boot) / (n * n))

    ci_lower = np.percentile(boots, 2.5)
    ci_upper = np.percentile(boots, 97.5)

    # Determine magnitude
    magnitude = ('Negligible' if abs(delta) < 0.147 else
                 'Small' if abs(delta) < 0.33 else
                 'Medium' if abs(delta) < 0.474 else
                 'Large')

    return delta, magnitude, [ci_lower, ci_upper]


# Function to compute per-snippet pass rates from test reports
def compute_pass_rates(test_report_df, rag_status):
    """
    Compute pass rates per snippet from test report.

    Parameters:
    -----------
    test_report_df : DataFrame
        Test report with columns: module, status, markers
    rag_status : str
        Either 'non_rag' or 'rag' to label columns

    Returns:
    --------
    DataFrame with columns: snippet, passed_*, failed_*, total_test_case_*, pass_rate_*
    """
    # Filter out xfail test cases
    test_report_df = test_report_df[test_report_df['markers'].isna()]

    final_list = []
    for snippet in test_report_df['module'].unique():
        snippet_name = snippet.split(".")[-1]
        snippet_data = test_report_df[test_report_df['module'] == snippet]

        passed = snippet_data[snippet_data['status'] == 'passed'].shape[0]
        failed = snippet_data[snippet_data['status'] == 'failed'].shape[0]
        total = passed + failed

        if total > 0:
            final_list.append([
                snippet_name,
                passed,
                failed,
                total,
                passed / total
            ])

    return pd.DataFrame(final_list, columns=[
        'snippet',
        f'passed_{rag_status}',
        f'failed_{rag_status}',
        f'total_test_case_{rag_status}',
        f'pass_rate_{rag_status}'
    ])


# Function to analyze RAG effect
def rag_effect(docstr_type, model):
    """
    Load and merge test reports for RAG and non-RAG conditions.

    Parameters:
    -----------
    docstr_type : str
        One of 'full_docstr', 'partial_docstr', 'no_docstr'
    model : str
        Model folder name

    Returns:
    --------
    DataFrame with merged pass rates for both conditions, or None if files not found
    """
    non_rag_path = f"../functional_correctness_test_folder/post_cut-off/{model}/{docstr_type}_reports/combined_test_report.csv"
    rag_path = f"../functional_correctness_test_folder/post_cut-off/rag/{model}/{docstr_type}_reports/combined_test_report.csv"

    try:
        non_rag_report_df = pd.read_csv(non_rag_path)
        rag_report_df = pd.read_csv(rag_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

    non_rag_per_snippet = compute_pass_rates(non_rag_report_df, 'non_rag')
    rag_per_snippet = compute_pass_rates(rag_report_df, 'rag')

    # Inner merge to ensure same snippets in both conditions
    return pd.merge(non_rag_per_snippet, rag_per_snippet, on='snippet', how='inner')


# Main analysis function
def rag_effect_report_generator(combined_report_df, model, docstr_type):
    """
    Perform statistical analysis comparing RAG vs non-RAG performance.

    Parameters:
    -----------
    combined_report_df : DataFrame
        Merged dataframe with pass rates for both conditions
    model : str
        Model name (for display)
    docstr_type : str
        Docstring type (for display)

    Returns:
    --------
    Dictionary with analysis results, or None if no data
    """
    if combined_report_df is None or combined_report_df.empty:
        print(f"No data for {model}, {docstr_type}")
        return None

    # Wilcoxon signed-rank test on pass rates (paired, two-sided)
    statistic, p_value = stats.wilcoxon(
        combined_report_df['pass_rate_non_rag'],
        combined_report_df['pass_rate_rag'],
        alternative='two-sided'
    )

    # Effect size (Cliff's Delta) on pass rates
    delta, magnitude, ci = cliffs_delta(
        combined_report_df['pass_rate_rag'],
        combined_report_df['pass_rate_non_rag']
    )

    # Differences based on pass rates (RAG - non-RAG)
    differences = combined_report_df['pass_rate_rag'] - combined_report_df['pass_rate_non_rag']
    mean_diff = np.mean(differences)
    median_diff = np.median(differences)
    improved = np.sum(differences > 0)
    worsened = np.sum(differences < 0)
    unchanged = np.sum(differences == 0)

    # Skewness and sign test
    skewness = stats.skew(differences)
    result = stats.binomtest(min(improved, worsened), improved + worsened, p=0.5) if improved + worsened > 0 else None
    sign_p = result.pvalue if result else 1.0

    # Power analysis for paired design
    n = len(combined_report_df)
    std_diff = np.std(differences)
    effect_size = abs(mean_diff) / std_diff if std_diff > 0 else 0

    # Use TTestPower for paired design (equivalent to one-sample t-test on differences)
    power_analyzer = TTestPower()
    try:
        power = power_analyzer.solve_power(
            effect_size=effect_size,
            nobs=n,  # For paired design, use total n (not nobs1)
            alpha=0.05,
            power=None,
            alternative='two-sided'
        )
    except:
        # If power calculation fails (e.g., effect size = 0), set to NaN
        power = np.nan

    # Results dictionary (raw p-value, FDR to be applied later)
    results = {
        'model': model_mapping[model],
        'docstr_type': docstr_type.replace('_docstr', ''),
        'mean_diff': mean_diff,
        'mean_diff_pct': mean_diff * 100,  # Convert to percentage (0-1 scale to 0-100)
        'median_diff': median_diff,
        'p_raw': p_value,
        'p_fdr': None,  # Placeholder, will be filled by FDR correction
        'cliffs_delta': delta,
        'cliffs_magnitude': magnitude,
        'cliffs_ci': ci,
        'improved': improved,
        'worsened': worsened,
        'unchanged': unchanged,
        'skewness': skewness,
        'sign_p': sign_p,
        'power': power
    }

    # Print detailed results
    print(
        f"Comparison between non-RAG and RAG-based generation for {model_mapping[model]} ({docstr_type.replace('_docstr', '')}):")
    print(f"  Wilcoxon: W={statistic:.1f}, p={p_value:.4f}")
    print(f"  Cliff's Delta: δ={delta:.3f} [{ci[0]:.3f}, {ci[1]:.3f}] ({magnitude})")
    print(f"  Mean difference: {mean_diff:.3f} ({results['mean_diff_pct']:.1f}%)")
    print(f"  Median difference: {median_diff:.3f}")
    print(f"  Improved: {improved}, Worsened: {worsened}, Unchanged: {unchanged}")
    print(f"  Skewness: {skewness:.3f}, Sign test p={sign_p:.4f}")
    print(f"  Power (d={effect_size:.2f}, n={n}): {power:.3f}")

    return results


if __name__ == "__main__":
    all_results = []

    # Process each docstring type separately
    for docstr_type in docstr_types:
        print(f"\n{'=' * 60}")
        print(f"Processing: {docstr_type}")
        print('=' * 60)

        raw_p_values = []
        docstr_results = []  # Store results for this docstring type

        # Collect results for all models with this docstring type
        for model in models:
            result = rag_effect_report_generator(rag_effect(docstr_type, model), model, docstr_type)
            if result:
                all_results.append(result)
                docstr_results.append(result)
                raw_p_values.append(result['p_raw'])

        # Apply FDR correction for this docstring type (7 tests)
        if raw_p_values:
            reject, p_fdr_adjusted, _, _ = multipletests(raw_p_values, alpha=0.05, method='fdr_bh')

            print(f"\n--- FDR Correction for {docstr_type} ---")
            print(f"Significant after FDR (α=0.05): {np.sum(reject)}/{len(reject)}")

            # Update the p_fdr values for this docstring type
            for i, result in enumerate(docstr_results):
                result['p_fdr'] = p_fdr_adjusted[i]
                if reject[i]:
                    print(f"  {result['model']}: p_raw={result['p_raw']:.4f}, p_fdr={p_fdr_adjusted[i]:.4f} ✓")

    # Save results to CSV
    results_df = pd.DataFrame(all_results)
    os.makedirs('../results/rq3/', exist_ok=True)
    results_df.to_csv('../results/rq3/rq3_results.csv', index=False)

    print(f"\n{'=' * 60}")
    print(f"Results saved to ../results/rq3/rq3_results.csv")
    print('=' * 60)

    # Print summary statistics
    print("\n--- Overall Summary ---")
    print(f"Total comparisons: {len(all_results)}")
    print(f"Significant (p_raw < 0.05): {sum(1 for r in all_results if r['p_raw'] < 0.05)}")
    print(f"Significant (p_fdr < 0.05): {sum(1 for r in all_results if r['p_fdr'] is not None and r['p_fdr'] < 0.05)}")
    print(f"Mean improvement across all: {np.mean([r['mean_diff_pct'] for r in all_results]):.2f}%")
    print(f"Total improved: {sum(r['improved'] for r in all_results)}")
    print(f"Total worsened: {sum(r['worsened'] for r in all_results)}")
    print(f"Total unchanged: {sum(r['unchanged'] for r in all_results)}")

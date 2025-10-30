import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.utils import resample
from statsmodels.stats.power import TTestIndPower


# Function to compute Cliff's Delta
def cliffs_delta(x, y):
    n_x, n_y = len(x), len(y)
    greater = sum(xi > yj for xi in x for yj in y)
    less = sum(xi < yj for xi in x for yj in y)
    delta = (greater - less) / (n_x * n_y)
    magnitude = 'negligible' if abs(delta) < 0.147 else 'small' if abs(delta) < 0.33 else 'medium' if abs(
        delta) < 0.474 else 'large'
    # Bootstrap CI for Cliff's Delta
    boot_deltas = []
    for _ in range(1000):
        s1, s2 = resample(x), resample(y)
        g = sum(xi > yj for xi in s1 for yj in s2)
        l = sum(xi < yj for xi in s1 for yj in s2)
        boot_deltas.append((g - l) / (len(s1) * len(s2)))
    ci = np.percentile(boot_deltas, [2.5, 97.5])
    return delta, magnitude, ci


# Function to compute bootstrap CI for mean difference
def bootstrap_ci_diff(data1, data2, n_boot=1000, alpha=0.05):
    diffs = []
    for _ in range(n_boot):
        s1, s2 = resample(data1), resample(data2)
        diffs.append(np.mean(s1) - np.mean(s2))
    return np.percentile(diffs, [100 * alpha / 2, 100 * (1 - alpha / 2)])


# Function to compute Cramér's V
def cramers_v(chi2, n, r, c):
    return np.sqrt(chi2 / (n * min(r - 1, c - 1)))


# Function to process test reports and compute per-snippet pass/fail counts
def docstr_effect(data_version, model):
    full_docstr_report_df = pd.read_csv(
        f"../functional_correctness_test_folder/{data_version}/{model}/full_docstr_reports/combined_test_report.csv")
    partial_docstr_report_df = pd.read_csv(
        f"../functional_correctness_test_folder/{data_version}/{model}/partial_docstr_reports/combined_test_report.csv")
    no_docstr_report_df = pd.read_csv(
        f"../functional_correctness_test_folder/{data_version}/{model}/no_docstr_reports/combined_test_report.csv")

    def snippet_wise_counts(test_report_df, docstr_type):
        test_report_df = test_report_df[test_report_df.markers.isnull()]
        final_list = []
        for snippet in test_report_df.module.unique():
            tmp_list = [snippet.split(".")[-1]]
            passed = \
                test_report_df[(test_report_df['module'] == snippet) & (test_report_df['status'] == 'passed')].shape[0]
            failed = \
                test_report_df[(test_report_df['module'] == snippet) & (test_report_df['status'] == 'failed')].shape[0]
            total = passed + failed
            if total > 0:
                tmp_list.extend([passed, failed, total, passed / total])
                final_list.append(tmp_list)
        return pd.DataFrame(final_list, columns=['snippet', f'passed_{docstr_type}', f'failed_{docstr_type}',
                                                 f'total_test_case_{docstr_type}', f'pass_rate_{docstr_type}'])

    full_docstr_per_snippet_report = snippet_wise_counts(full_docstr_report_df, 'full')
    partial_docstr_per_snippet_report = snippet_wise_counts(partial_docstr_report_df, 'partial')
    no_docstr_per_snippet_report = snippet_wise_counts(no_docstr_report_df, 'no')

    # Validate snippet alignment
    snippets_full = set(full_docstr_per_snippet_report['snippet'])
    snippets_partial = set(partial_docstr_per_snippet_report['snippet'])
    snippets_no = set(no_docstr_per_snippet_report['snippet'])
    common_snippets = snippets_full.intersection(snippets_partial, snippets_no)
    print(f"Common snippets for {model} ({data_version}): {len(common_snippets)}")
    if len(common_snippets) < min(len(snippets_full), len(snippets_partial), len(snippets_no)):
        print(
            f"Warning: Dropped snippets - Full: {len(snippets_full)}, Partial: {len(snippets_partial)}, No: {len(snippets_no)}")

    merged_df = pd.merge(full_docstr_per_snippet_report, partial_docstr_per_snippet_report, on='snippet',
                         how='inner').merge(no_docstr_per_snippet_report, on='snippet', how='inner')
    return merged_df


# Function to generate ablation study report
def ablation_study_report_generator(combined_report_df, model, dataset):
    results = []

    # Friedman Test (three-way comparison: full, partial, no docstrings)
    try:
        stat, p_value = stats.friedmanchisquare(
            combined_report_df.pass_rate_full,
            combined_report_df.pass_rate_partial,
            combined_report_df.pass_rate_no
        )
        results.append({
            'model': model,
            'dataset': dataset,
            'comparison': 'friedman_all',
            'stat': stat,
            'p_value': p_value
        })
        print(f"Friedman Test for {model} ({dataset}): stat={stat:.4f}, p={p_value:.4e}")
    except Exception as e:
        print(f"Friedman Test failed for {model} ({dataset}): {e}")

    # FIXED: Use actual mean test count for percentage calculation
    mean_test_count = combined_report_df['total_test_case_full'].mean()

    # Wilcoxon Tests with Assumption Validation
    comparisons = [('full_vs_partial', 'pass_rate_full', 'pass_rate_partial'),
                   ('full_vs_no', 'pass_rate_full', 'pass_rate_no')]
    for comp, col1, col2 in comparisons:
        differences = np.array(combined_report_df[col2]) - np.array(combined_report_df[col1])
        skewness = stats.skew(differences)
        print(f"Skewness of differences for {comp} ({model}, {dataset}): {skewness:.4f}")
        if abs(skewness) > 1:
            print(f"Warning: High skewness in {comp}, consider sign test")
            # Sign test as fallback
            n_positive = np.sum(differences > 0)
            n_negative = np.sum(differences < 0)
            sign_test = stats.binomtest(min(n_positive, n_negative), n_positive + n_negative, p=0.5)
            sign_p = sign_test.pvalue
        else:
            sign_p = None

        statistic, p_value = stats.wilcoxon(combined_report_df[col1], combined_report_df[col2])
        delta, magnitude, delta_ci = cliffs_delta(combined_report_df[col1], combined_report_df[col2])
        diff_ci = bootstrap_ci_diff(combined_report_df[col1], combined_report_df[col2])

        results.append({
            'model': model,
            'dataset': dataset,
            'comparison': comp,
            'p_value': p_value,
            'mean_diff': np.mean(differences),
            'mean_diff_percent': np.mean(differences) / mean_test_count * 100,  # FIXED: Use actual mean test count
            'median_diff': np.median(differences),
            'n_worsened': np.sum(differences < 0),
            'n_improved': np.sum(differences > 0),
            'n_unchanged': np.sum(differences == 0),
            'cliffs_delta': delta,
            'delta_magnitude': magnitude,
            'delta_ci': delta_ci,
            'diff_ci': diff_ci,
            'skewness': skewness,
            'sign_test_p': sign_p
        })
        print(f"{comp} for {model} ({dataset}):")
        print(
            f"  p={p_value:.4f}, mean_diff={np.mean(differences):.3f} ({np.mean(differences) / mean_test_count * 100:.2f}%), cliffs_delta={delta:.3f} ({magnitude})")

    # Pooled Chi-Square Analysis
    pooled_data = {
        'full': {'passed': combined_report_df.passed_full.sum(), 'failed': combined_report_df.failed_full.sum()},
        'partial': {'passed': combined_report_df.passed_partial.sum(),
                    'failed': combined_report_df.failed_partial.sum()},
        'no': {'passed': combined_report_df.passed_no.sum(), 'failed': combined_report_df.failed_no.sum()}
    }
    for comp in ['full_vs_partial', 'full_vs_no']:
        cond1, cond2 = comp.split('_vs_')
        contingency = np.array([
            [pooled_data[cond1]['passed'], pooled_data[cond1]['failed']],
            [pooled_data[cond2]['passed'], pooled_data[cond2]['failed']]
        ])
        chi2, p_value, _, _ = stats.chi2_contingency(contingency)
        n = contingency.sum()
        v = cramers_v(chi2, n, 2, 2)
        rate1 = pooled_data[cond1]['passed'] / (pooled_data[cond1]['passed'] + pooled_data[cond1]['failed']) * 100
        rate2 = pooled_data[cond2]['passed'] / (pooled_data[cond2]['passed'] + pooled_data[cond2]['failed']) * 100
        diff = rate1 - rate2
        # Bootstrap CI for proportion difference
        diffs = []
        for _ in range(1000):
            s1 = np.random.binomial(pooled_data[cond1]['passed'] + pooled_data[cond1]['failed'], rate1 / 100)
            s2 = np.random.binomial(pooled_data[cond2]['passed'] + pooled_data[cond2]['failed'], rate2 / 100)
            diffs.append((s1 / (pooled_data[cond1]['passed'] + pooled_data[cond1]['failed']) - s2 / (
                    pooled_data[cond2]['passed'] + pooled_data[cond2]['failed'])) * 100)
        diff_ci = np.percentile(diffs, [2.5, 97.5])

        results.append({
            'model': model,
            'dataset': dataset,
            'comparison': f"chi2_{comp}",
            'chi2': chi2,
            'p_value': p_value,
            'cramers_v': v,
            'rate1': rate1,
            'rate2': rate2,
            'diff': diff,
            'diff_ci': diff_ci
        })
        print(f"Pooled Chi-Square for {comp} ({model}, {dataset}):")
        print(f"  χ²={chi2:.2f}, p={p_value:.4e}, Cramér's V={v:.3f}")

    # Power Analysis for Wilcoxon Tests
    power_analysis = TTestIndPower()
    effect_size = 0.3  # Small-medium effect (based on RQ2 draft)
    nobs = len(combined_report_df)
    power = power_analysis.power(effect_size, nobs1=nobs, ratio=1, alpha=0.05, alternative='two-sided')
    results.append({
        'model': model,
        'dataset': dataset,
        'comparison': 'power_analysis',
        'power': power
    })
    print(f"Power Analysis for {model} ({dataset}): {power:.3f}")

    return results


# Function for temporal analysis
def temporal_analysis(results_df):
    temporal_results = []
    for model in results_df['model'].unique():
        model_df = results_df[results_df['model'] == model]
        for comp in ['full_vs_partial', 'full_vs_no']:
            pre_df = model_df[(model_df['dataset'] == 'csn') & (model_df['comparison'] == comp)]
            post_df = model_df[(model_df['dataset'] == 'post_cut-off') & (model_df['comparison'] == comp)]
            if not pre_df.empty and not post_df.empty:
                benefit_ratio_pre = pre_df['n_improved'].iloc[0] / (pre_df['n_worsened'].iloc[0] + 1e-10)
                benefit_ratio_post = post_df['n_improved'].iloc[0] / (post_df['n_worsened'].iloc[0] + 1e-10)
                # FIXED: Handle division by zero for net benefit calculation
                net_benefit_pre = pre_df['n_improved'].iloc[0] / (pre_df['n_unchanged'].iloc[0] + 1e-10) * 100
                net_benefit_post = post_df['n_improved'].iloc[0] / (post_df['n_unchanged'].iloc[0] + 1e-10) * 100
                temporal_results.append({
                    'model': model,
                    'comparison': comp,
                    'benefit_ratio_pre': benefit_ratio_pre,
                    'benefit_ratio_post': benefit_ratio_post,
                    'net_benefit_pre': net_benefit_pre,
                    'net_benefit_post': net_benefit_post
                })
    temporal_df = pd.DataFrame(temporal_results)
    if not temporal_df.empty:
        stat, p_value = stats.wilcoxon(temporal_df['benefit_ratio_pre'], temporal_df['benefit_ratio_post'])
        print(f"Temporal Analysis (Wilcoxon): stat={stat:.4f}, p={p_value:.4e}")
        temporal_df['temporal_p'] = p_value
    return temporal_df


if __name__ == "__main__":
    models = ['codestral', 'gpt-4.1', 'gpt-5', 'meta-llama', 'deepseek-ai', 'openai', 'Qwen']

    # Collect all results first
    all_results_combined = []

    for data_version in ['csn', 'post_cut-off']:
        for model in models:
            try:
                combined_report_df = docstr_effect(data_version, model)
                # Check test count consistency
                test_counts = combined_report_df[
                    ['total_test_case_full', 'total_test_case_partial', 'total_test_case_no']].describe()
                print(f"Test count summary for {model} ({data_version}):\n{test_counts}")
                results = ablation_study_report_generator(combined_report_df, model, data_version)
                all_results_combined.extend(results)
            except FileNotFoundError as e:
                print(f"Files for {model} ({data_version}) not found: {e}")
                continue

    # Apply FDR correction separately per dataset (treating pre-cutoff and post-cutoff as independent experiments)
    results_df = pd.DataFrame(all_results_combined)

    print("\n=== Applying FDR Correction Separately Per Dataset ===")

    # Initialize lists to collect corrected results
    corrected_results = []

    # Process each dataset separately
    for dataset in ['csn', 'post_cut-off']:
        dataset_results = results_df[results_df['dataset'] == dataset].copy()

        print(f"\n--- Dataset: {dataset} ---")

        # 1. FDR for Friedman tests (7 tests per dataset: 7 models)
        friedman_tests = dataset_results[dataset_results['comparison'] == 'friedman_all'].copy()
        if not friedman_tests.empty:
            reject, p_fdr, _, _ = multipletests(friedman_tests['p_value'], method='fdr_bh', alpha=0.05)
            friedman_tests['p_fdr'] = p_fdr
            friedman_tests['significant_fdr'] = reject
            print(f"Friedman tests ({dataset}): Significant after FDR: {reject.sum()}/{len(reject)}")
            corrected_results.append(friedman_tests)

        # 2. FDR for Wilcoxon tests (14 tests per dataset: 7 models × 2 comparisons)
        wilcoxon_tests = dataset_results[dataset_results['comparison'].isin(['full_vs_partial', 'full_vs_no'])].copy()
        if not wilcoxon_tests.empty:
            reject, p_fdr, _, _ = multipletests(wilcoxon_tests['p_value'], method='fdr_bh', alpha=0.05)
            wilcoxon_tests['p_fdr'] = p_fdr
            wilcoxon_tests['significant_fdr'] = reject
            print(f"Wilcoxon tests ({dataset}): Significant after FDR: {reject.sum()}/{len(reject)}")

            # Also apply FDR to sign tests if they were used
            sign_test_mask = wilcoxon_tests['sign_test_p'].notna()
            if sign_test_mask.any():
                sign_p_values = wilcoxon_tests.loc[sign_test_mask, 'sign_test_p']
                reject_sign, p_fdr_sign, _, _ = multipletests(sign_p_values, method='fdr_bh', alpha=0.05)
                wilcoxon_tests.loc[sign_test_mask, 'sign_test_p_fdr'] = p_fdr_sign
                wilcoxon_tests.loc[sign_test_mask, 'sign_test_significant_fdr'] = reject_sign
                print(
                    f"Sign tests ({dataset}): Used for {sign_test_mask.sum()} comparisons, Significant after FDR: {reject_sign.sum()}")

            corrected_results.append(wilcoxon_tests)

        # 3. FDR for Chi-square tests (14 tests per dataset: 7 models × 2 comparisons)
        chi2_tests = dataset_results[dataset_results['comparison'].str.startswith('chi2_')].copy()
        if not chi2_tests.empty:
            reject, p_fdr, _, _ = multipletests(chi2_tests['p_value'], method='fdr_bh', alpha=0.05)
            chi2_tests['p_fdr'] = p_fdr
            chi2_tests['significant_fdr'] = reject
            print(f"Chi-square tests ({dataset}): Significant after FDR: {reject.sum()}/{len(reject)}")
            corrected_results.append(chi2_tests)

        # Add power analysis results (no FDR correction needed)
        power_results = dataset_results[dataset_results['comparison'] == 'power_analysis'].copy()
        if not power_results.empty:
            corrected_results.append(power_results)

    # Combine all corrected results
    final_df = pd.concat(corrected_results, ignore_index=True)

    # Print summary
    print("\n=== Summary of Significant Results (FDR < 0.05 per dataset) ===")
    if 'significant_fdr' in final_df.columns:
        sig_results = final_df[final_df['significant_fdr'] == True]
        if not sig_results.empty:
            for _, row in sig_results.iterrows():
                print(
                    f"{row['model']} ({row['dataset']}) - {row['comparison']}: p={row['p_value']:.4f}, p_fdr={row['p_fdr']:.4f}")
        else:
            print("No results significant after FDR correction")

    # Temporal Analysis
    temporal_df = temporal_analysis(final_df)
    if not temporal_df.empty:
        temporal_df.to_csv('../results/rq2/temporal_docstring_analysis.csv', index=False)

    # Export Results
    final_df.to_csv('../results/rq2/docstring_ablation_results.csv', index=False)
    print("\nResults saved to ../results/rq2/docstring_ablation_results.csv")

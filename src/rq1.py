import pandas as pd
import numpy as np
from scipy.stats import kruskal, mannwhitneyu, chi2_contingency
from statsmodels.stats.multitest import multipletests
from sklearn.utils import resample
from statsmodels.stats.power import TTestIndPower
from statsmodels.formula.api import mixedlm
from scipy.stats import shapiro


def test_normality(data):
    stat, p = shapiro(data)
    print('W-statistic=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:  # FIXED: Removed Bonferroni correction for diagnostic test
        print("Data looks normal (fail to reject H₀)")
    else:
        print("Data does not look normal (reject H₀)")


def process_und(report_path):
    report_df = pd.read_csv(report_path)
    report_df = report_df[report_df['Kind'].isin(["Class", "Abstract Class"])]
    report_df['snippet'] = [snip.split(".py")[0].split("snippet_")[1] for snip in report_df['File']]
    report_df.dropna(inplace=True, axis=1)
    return report_df


def pooled_data_generation(path_to_combined_report):
    df = pd.read_csv(path_to_combined_report)
    df = df[df.markers.isnull()]
    total_tests = len(df)
    passed_tests = len(df[df['status'] == 'passed'])
    failed_tests = len(df[df['status'] == 'failed'])

    return {'total': total_tests, 'passed': passed_tests, 'failed': failed_tests}


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


# Function to process CSV and compute per-class pass rates and test case count
def process_csv(file_path, dataset_name):
    try:
        df = pd.read_csv(file_path)
        # Filter where markers is null or empty
        df = df[df['markers'].isna() | (df['markers'] == '')]
        # Extract snippet number from 'file' column
        df['snippet'] = df['file'].str.extract(r'test_snippet_(\d+)\.py', expand=False)
        df = df.dropna(subset=['snippet'])
        # Group by snippet
        grouped = df.groupby('snippet')
        # Compute passed and total test cases
        passed = grouped['status'].apply(lambda x: (x == 'passed').sum())
        total = grouped.size()
        pass_rate = passed / total
        # Create DataFrame
        result_df = pd.DataFrame({
            'snippet': pass_rate.index,
            'pass_rate': pass_rate.values,
            'test_count': total.values,
            'dataset': dataset_name
        })
        return result_df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


# Function for pooled chi-square analysis
def cramers_v(chi2, n, r, c):
    return np.sqrt(chi2 / (n * min(r - 1, c - 1)))


def compare_datasets_pooled(model_name, dataset1, dataset2, data1, data2):
    passed1 = data1['passed']
    failed1 = data1['total'] - data1['passed']
    passed2 = data2['passed']
    failed2 = data2['total'] - data2['passed']
    contingency = np.array([[passed1, failed1], [passed2, failed2]])
    chi2, p_value, _, _ = chi2_contingency(contingency)
    n = contingency.sum()
    v = cramers_v(chi2, n, 2, 2)
    rate1 = passed1 / data1['total'] * 100
    rate2 = passed2 / data2['total'] * 100
    diff = rate1 - rate2
    # Bootstrap CI for proportion difference
    diffs = []
    for _ in range(1000):
        s1 = np.random.binomial(data1['total'], rate1 / 100)
        s2 = np.random.binomial(data2['total'], rate2 / 100)
        diffs.append((s1 / data1['total'] - s2 / data2['total']) * 100)
    ci = np.percentile(diffs, [2.5, 97.5])
    return {
        'model': model_name,
        'comparison': f"{dataset1} vs {dataset2}",
        'rate1': rate1,
        'rate2': rate2,
        'diff': diff,
        'diff_ci': ci,
        'chi2': chi2,
        'p_value': p_value,
        'cramers_v': v
    }


if __name__ == '__main__':
    pooled_data = {}
    models = ['Qwen', 'gpt-4.1', 'gpt-5', 'deepseek-ai', 'openai', 'meta-llama', 'codestral']
    all_results = []
    pooled_results = []
    all_pvalues_perclass = []  # FIXED: Collect all p-values for FDR correction
    all_power_results = []  # FIXED: Collect power analysis for all models

    for model in models:
        print(f"\n=== Analysis for Model: {model.upper()} ===")

        classeval_file = f'../functional_correctness_test_folder/ClassEval/{model}/full_docstr_reports/combined_test_report.csv'
        csn_file = f'../functional_correctness_test_folder/csn/{model}/full_docstr_reports/combined_test_report.csv'
        post_cutoff_file = f'../functional_correctness_test_folder/post_cut-off/{model}/full_docstr_reports/combined_test_report.csv'

        classeval_und_file = f'../../../../MISC_use/run_understand/ClassEval/{model}/{model}.csv'
        csn_und_file = f'../../../../MISC_use/run_understand/csn/{model}/{model}.csv'
        post_cutoff_und_file = f'../../../../MISC_use/run_understand/post_cut-off/{model}/{model}.csv'

        pooled_data[model] = {'ClassEval': pooled_data_generation(classeval_file),
                              'csn': pooled_data_generation(csn_file),
                              'post_cut-off': pooled_data_generation(post_cutoff_file)}

        # Load and process CSV files (adjust paths as needed)
        try:
            classeval_df = process_csv(classeval_file, 'ClassEval').merge(process_und(classeval_und_file), on='snippet',
                                                                          how='inner')
            csn_df = process_csv(csn_file, 'csn').merge(process_und(csn_und_file), on='snippet', how='inner')
            post_cutoff_df = process_csv(post_cutoff_file, 'post_cut-off').merge(process_und(post_cutoff_und_file),
                                                                                 on='snippet', how='inner')

            # Combine data
            all_df = pd.concat([classeval_df, csn_df, post_cutoff_df])
            all_df['model'] = model

            # FIXED: Kruskal-Wallis Test (instead of Friedman)
            pass_rates_classeval = all_df[all_df['dataset'] == 'ClassEval']['pass_rate']
            test_normality(pass_rates_classeval)
            pass_rates_csn = all_df[all_df['dataset'] == 'csn']['pass_rate']
            test_normality(pass_rates_csn)
            pass_rates_post = all_df[all_df['dataset'] == 'post_cut-off']['pass_rate']
            test_normality(pass_rates_post)

            # FIXED: Use Kruskal-Wallis for independent samples (no truncation needed)
            stat, p = kruskal(pass_rates_classeval, pass_rates_csn, pass_rates_post)
            print(f"Kruskal-Wallis Test: stat={stat:.4f}, p={p:.4e}")

            # Pairwise Mann-Whitney U Tests
            pairs = [('ClassEval', 'csn'), ('ClassEval', 'post_cut-off'), ('csn', 'post_cut-off')]
            pairwise_results = []
            for d1, d2 in pairs:
                group1 = all_df[all_df['dataset'] == d1]['pass_rate']
                group2 = all_df[all_df['dataset'] == d2]['pass_rate']
                u_stat, p_val = mannwhitneyu(group1, group2, alternative='two-sided')
                diff_ci = bootstrap_ci_diff(group1, group2)
                delta, magnitude, delta_ci = cliffs_delta(group1, group2)
                pairwise_results.append({
                    'model': model,
                    'comparison': f"{d1} vs {d2}",
                    'u_stat': u_stat,
                    'p_value': p_val,
                    'diff': group1.mean() - group2.mean(),
                    'diff_ci': diff_ci,
                    'cliffs_delta': delta,
                    'delta_magnitude': magnitude,
                    'delta_ci': delta_ci
                })
                all_pvalues_perclass.append(p_val)  # FIXED: Collect for global FDR
                print(f"Mann-Whitney U for {d1} vs {d2}: U={u_stat:.4f}, p={p_val:.4e}")
                print(f"Mean Diff: {group1.mean() - group2.mean():.4f}, 95% CI: {diff_ci}")
                print(f"Cliff's Delta: {delta:.4f} ({magnitude}), 95% CI: {delta_ci}")

            # FIXED: Power Analysis for all models
            power_analysis = TTestIndPower()
            effect_size = 0.5  # Medium effect (based on Cliff's Delta)
            n1 = len(all_df[all_df['dataset'] == 'ClassEval'])
            n2 = len(all_df[all_df['dataset'] == 'csn'])
            ratio = n2 / n1
            power = power_analysis.power(effect_size, nobs1=n1, ratio=ratio, alpha=0.05, alternative='two-sided')
            all_power_results.append({'model': model, 'power': power})
            print(f"\nPower Analysis (ClassEval vs csn): {power:.3f}")

            # Pooled Chi-Square Analysis
            datasets = pooled_data[model]
            for d1, d2 in pairs:
                result = compare_datasets_pooled(model, d1, d2, datasets[d1], datasets[d2])
                pooled_results.append(result)
                print(f"\nPooled Chi-Square for {d1} vs {d2}:")
                print(f"  Pass Rate {d1}: {result['rate1']:.2f}%")
                print(f"  Pass Rate {d2}: {result['rate2']:.2f}%")
                print(f"  Diff: {result['diff']:.2f}%, 95% CI: {result['diff_ci']}")
                print(
                    f"  χ² = {result['chi2']:.2f}, p = {result['p_value']:.4e}, Cramér's V = {result['cramers_v']:.3f}")

            # Store results
            all_results.extend(pairwise_results)
            all_df.to_csv(f'{model}_pass_rates.csv')

        except FileNotFoundError as e:
            print(f"Files for {model} not found: {e}")
            continue

    # FIXED: Apply FDR correction across all 21 tests
    print("\n=== Applying FDR Correction Across All Per-Class Tests ===")
    reject_perclass, p_adjusted_perclass, _, _ = multipletests(all_pvalues_perclass, alpha=0.05, method='fdr_bh')

    # Add FDR-adjusted p-values back to results
    for i, result in enumerate(all_results):
        result['p_fdr'] = p_adjusted_perclass[i]
        result['significant'] = reject_perclass[i]

    # Print results with FDR correction
    results_df = pd.DataFrame(all_results)
    print(results_df[['model', 'comparison', 'diff', 'p_value', 'p_fdr', 'cliffs_delta', 'delta_magnitude']].to_string(
        index=False))

    # FDR Correction for Pooled Chi-Square
    pooled_df = pd.DataFrame(pooled_results)
    pooled_df['p_fdr'] = multipletests(pooled_df['p_value'], method='fdr_bh')[1]
    print("\n=== Pooled Chi-Square Results (FDR-corrected) ===")
    print(pooled_df[['model', 'comparison', 'diff', 'p_value', 'p_fdr', 'cramers_v', 'diff_ci']].to_string(index=False))

    # FIXED: Mixed-Effects Model on combined data (outside loop)
    all_dfs = [pd.read_csv(f'{model}_pass_rates.csv') for model in models if
               pd.io.common.file_exists(f'{model}_pass_rates.csv')]
    combined_df = pd.concat(all_dfs)

    try:
        combined_df['pass_rate_transformed'] = np.arcsin(np.sqrt(combined_df['pass_rate']))
        model_mixed = mixedlm(
            "pass_rate_transformed ~ dataset + test_count + CountLineCode + AvgCyclomatic + CountClassCoupled + CountDeclMethod",
            data=combined_df, groups=combined_df['model'])
        result_mixed = model_mixed.fit()
        print("\n=== Mixed-Effects Model Summary (fitted on all models) ===")
        print(result_mixed.summary())
    except Exception as e:
        print(f"Mixed-Effects Model failed: {e}")

    # Summary Statistics
    summary = combined_df.groupby(['model', 'dataset'])['pass_rate'].agg(['mean', 'median', 'std', 'count'])
    print("\n=== Summary Statistics ===")
    print(summary)

    # FIXED: Power Analysis Summary
    power_df = pd.DataFrame(all_power_results)
    print("\n=== Power Analysis Summary (ClassEval vs csn) ===")
    print(power_df.to_string(index=False))
    print(f"Power Range: {power_df['power'].min():.3f} - {power_df['power'].max():.3f}")

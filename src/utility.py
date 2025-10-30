from os import listdir
from os.path import isfile, join
import os, ast, re
import pandas as pd
from typing import Dict

path_to_data = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))


def list_files(folder_path, all_files=True, extension=None):
    """List files in a folder, optionally filtering by extension."""
    if all_files:
        return [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    else:
        if extension is None:
            raise ValueError("Extension cannot be None if only a fixed type of files are to be listed.")
        else:
            return [f for f in listdir(folder_path) if (isfile(join(folder_path, f)) and f.endswith(f".{extension}"))]


def total_program_unit_fixer(code: str) -> Dict[str, int]:
    """
    Count the number of classes and functions in Python code.

    Args:
        code: Python source code as a string

    Returns:
        Dictionary with counts: {'classes': int, 'functions': int, 'async_functions': int}
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {'classes': 0, 'functions': 0, 'async_functions': 0}

    class_count = 0
    function_count = 0
    async_function_count = 0

    # Walk through AST and count each node type
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_count += 1
        elif isinstance(node, ast.FunctionDef):
            function_count += 1
        elif isinstance(node, ast.AsyncFunctionDef):
            async_function_count += 1

    return class_count + function_count + async_function_count


def refine_indentation(skeleton):
    """Fix indentation issues in Python code skeletons by standardizing spacing and adding pass statements."""
    try:
        skeleton = skeleton.rstrip()
        lines = skeleton.replace("\t", " " * 4).split("\n")

        # Ensure last line is 'pass'
        if lines[-1].strip() != "pass":
            lines.append("pass")

        # Fix indentation of pass statements based on their corresponding def/class
        for i in range(len(lines)):
            if lines[i].strip() == "pass":
                def_line = [l for l in lines[i::-1] if (l.lstrip()[:3] == 'def' or l.lstrip()[:5] == 'class')][0]
                leading_spaces = len(def_line) - len(def_line.lstrip(' '))
                if leading_spaces == 0:
                    lines[i] = " " * 4 + "pass"
                else:
                    lines[i] = " " * 2 * leading_spaces + "pass"

        # Handle class-only skeletons
        if "def" not in skeleton and "pass" not in skeleton:
            if skeleton.split().count("class") == 1:
                lines.append(" " * 4 + "pass")
            else:
                return None

        # Remove duplicate pass statements
        for i in range(len(lines)):
            if 'pass' in lines[i] and 'pass' in lines[i - 1]:
                del lines[i]

        # Fix docstring indentation
        for i in range(len(lines)):
            if ("'''" in lines[i] or '"""' in lines[i]) and ('def' in lines[i - 1] or 'class' in lines[i - 1]):
                lines[i] = " " * (len(lines[i - 1]) - len(lines[i - 1].lstrip(' ')) + 4) + lines[i].lstrip()
            if ("'''" in lines[i] or '"""' in lines[i]) and 'pass' in lines[i + 1]:
                lines[i] = " " * (len(lines[i + 1]) - len(lines[i + 1].lstrip(' '))) + lines[i].lstrip()

        refined_skeleton = "\n".join(lines)
        refined_skeleton = refined_skeleton.replace("\n\n", "\n")
        return refined_skeleton
    except:
        return None


def combine_understand_reports(data_version: str) -> pd.DataFrame:
    """Combine Understand analysis reports for all successfully analyzed projects, filtering for class definitions."""
    report_file_list = []

    # Load and filter for successfully analyzed projects
    und_analysis_df = pd.read_csv(
        f"{path_to_data}/metadata_folder/{data_version}/file_mapping_with_analysis_status.csv")
    und_analysis_df = und_analysis_df[und_analysis_df['analysis_status'] == 'Successfull']

    # Process each project's analysis report
    for _, row in und_analysis_df.iterrows():
        try:
            tmp_df = pd.read_csv(
                f"{path_to_data}/metadata_folder/{data_version}/Understand_analysis_reports/{row['expected_analysis_report_file']}",
                low_memory=False)
            # Filter for class definitions only
            tmp_class_df = tmp_df[(tmp_df['Kind'] == "Class") | (tmp_df['Kind'] == "Abstract Class")]
            tmp_class_df['report_file_name'] = [row['expected_analysis_report_file']] * tmp_class_df.shape[0]
            tmp_class_df['repo_name'] = [row['repo_name']] * tmp_class_df.shape[0]
            report_file_list.append(tmp_class_df)
        except Exception as e:
            print(str(e))

    analysis_report_df = pd.concat(report_file_list, axis=0)

    print(f"Total number of classes to be processed is {analysis_report_df.shape[0]}")

    return analysis_report_df


def snippet_cleaning(raw_snippet):
    """Remove leading whitespace from code snippets while preserving relative indentation."""
    leading_spaces = len(raw_snippet) - len(raw_snippet.lstrip())
    if leading_spaces == 0:
        clean_snippet = raw_snippet
    else:
        clean_snippet = ""
        for line in raw_snippet.split("\n"):
            clean_snippet += line[leading_spaces:] + "\n"
    return clean_snippet


def match_valid_multiline_comments(code_text):
    """Find all valid multiline comments (triple-quoted strings) that are not string assignments."""
    code_text = code_text.replace("= ", "=")

    regex_pattern = r"([\'\"])\1\1[\d\D]*?\1{3}"

    matches = re.finditer(regex_pattern, code_text, re.MULTILINE)
    valid_multiline_comments = []
    for match in matches:
        # Include if at start of code or not preceded by '=' (not an assignment)
        if match.span()[0] == 0:
            valid_multiline_comments.append(match.group())
        else:
            if code_text[match.span()[0] - 1] != '=':
                valid_multiline_comments.append(match.group())
            else:
                continue

    return valid_multiline_comments


def remove_multiline_comments(code_text):
    """Remove all valid multiline comments from code text."""
    cleaned_code_text = code_text
    for multiline_comment in match_valid_multiline_comments(code_text):
        cleaned_code_text = cleaned_code_text.replace(multiline_comment, "")

    return cleaned_code_text

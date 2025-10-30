import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import os, ast, subprocess, re, autopep8
from utility import combine_understand_reports

path_to_data = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def snippet_cleaning(raw_snippet):
    leading_spaces = len(raw_snippet) - len(raw_snippet.lstrip())
    if leading_spaces == 0:
        clean_snippet = raw_snippet
    else:
        clean_snippet = ""
        for line in raw_snippet.split("\n"):
            clean_snippet += line[leading_spaces:] + "\n"
    return clean_snippet


def extract_class_with_imports(source_code: str, class_name: str) -> str:
    tree = ast.parse(source_code)

    # --- Step 1: Collect imports
    imports = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(node)

    # --- Step 2: Find target class
    target_class = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            target_class = node
            break
    if not target_class:
        raise ValueError(f"Class {class_name} not found")

    # --- Step 3: Collect names used in the class
    used_names = set()

    class ImportNameCollector(ast.NodeVisitor):
        def visit_Name(self, node):
            used_names.add(node.id)
        def visit_Attribute(self, node):
            # Capture base name in expressions like os.path.join
            while isinstance(node, ast.Attribute):
                node = node.value
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            self.generic_visit(node)

    ImportNameCollector().visit(target_class)

    # --- Step 4: Select only the needed imports
    needed_imports = []
    for imp in imports:
        if isinstance(imp, ast.Import):
            for alias in imp.names:
                if alias.asname in used_names or alias.name.split(".")[0] in used_names:
                    needed_imports.append(imp)
        elif isinstance(imp, ast.ImportFrom):
            for alias in imp.names:
                if alias.asname in used_names or alias.name in used_names:
                    needed_imports.append(imp)

    needed_imports = list(set(needed_imports)) # so that same import is not present twice
    # --- Step 5: Reconstruct code
    selected_nodes = needed_imports + [target_class]
    new_module = ast.Module(body=selected_nodes, type_ignores=[])

    return ast.unparse(new_module)

def extract_skeleton(class_code_snippet):
    class_signatures = [match.group() for _, match in enumerate(
        re.finditer(r"^\s*class\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(*[\s\S]*?\)*[\s\S]*?:",
                    class_code_snippet, re.MULTILINE),
        start=1)]
    func_signatures = [match.group() for _, match in enumerate(
        re.finditer(r"^\s*(?:async\s+)?def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([\s\S]*?\)[\s\S]*?:",
                    class_code_snippet, re.MULTILINE),
        start=1)]
    tree = ast.parse(class_code_snippet)
    skeleton_dict = {}
    for node in ast.walk(tree):
        if type(node).__name__ == "ClassDef":
            sub_skeleton = ""
            code_segment = [signature for signature in class_signatures if "class " + node.name in signature][0]
            leading_spaces = len(code_segment) - len(code_segment.lstrip(" "))
            sub_skeleton += code_segment + "\n"
            if ast.get_docstring(node, clean=False) is not None:
                docstring = "\t'''"
                docstring += ast.get_docstring(node, clean=False) + "'''"
                sub_skeleton += docstring
            sub_skeleton += "\n"
            skeleton_dict[node.lineno] = sub_skeleton
            if len(node.decorator_list) > 0:
                for dec in node.decorator_list:
                    skeleton_dict[dec.lineno] = (" " * leading_spaces) + "@" + ast.get_source_segment(
                        class_code_snippet, dec, padded=False)

        if type(node).__name__ == "FunctionDef" or type(node).__name__ == "AsyncFunctionDef":
            sub_skeleton = ""
            code_segment = [signature for signature in func_signatures if "def " + node.name in signature][0]
            leading_spaces = len(code_segment) - len(code_segment.lstrip(" "))
            sub_skeleton += code_segment + "\n"
            if ast.get_docstring(node, clean=False) is not None:
                docstring = "\t'''"
                docstring += ast.get_docstring(node, clean=False) + "'''"
                sub_skeleton += docstring + "\n\t"
            sub_skeleton += "pass\n"
            skeleton_dict[node.lineno] = sub_skeleton
            if len(node.decorator_list) > 0:
                for dec in node.decorator_list:
                    skeleton_dict[dec.lineno] = (" " * leading_spaces) + "@" + ast.get_source_segment(
                        class_code_snippet, dec, padded=False)

    skeleton = ""
    docstr_counter = 0
    for key, value in dict(sorted(skeleton_dict.items())).items():
        skeleton += value + "\n"
        if "\t'''" in value:
            docstr_counter += 1
    if len(skeleton_dict) == 1:
        skeleton += "\tpass"
    return skeleton, len(skeleton_dict), docstr_counter


def class_skeleton_extractor():
    full_class_df = combine_understand_reports()
    unique_projects = full_class_df['repo_name'].unique()
    full_data_list = []
    fail_counter = 0
    fail_log_dict = {}
    successful_process_logger = open(f"{path_to_data}/metadata_folder/skeleton_extraction_success.log", 'a')
    successful_process_logger.write("repo,number_classes,number_of_processed_classes\n")
    total_counter = 0
    for repo in unique_projects: # change here
        success_counter = 0
        proj_df = full_class_df[full_class_df["repo_name"] == repo]
        proj_df.drop_duplicates(keep='last', inplace=True)
        repo_folder = repo.replace("/", "_")
        subprocess.run(f"git clone https://github.com/{repo}.git {path_to_data}/git_repos_for_analysis/{repo_folder}",
                       shell=True)
        for _, row in proj_df.iterrows():
            total_counter += 1
            proj_data_list = [row['repo_name'], row['File'], row['Name'], row['RatioCommentToCode']]
            try:
                file_name = row['File'] if repo_folder in row['File'] else f"{repo_folder}/{row['File']}"
                f = open(f"{path_to_data}/git_repos_for_analysis/{file_name}", 'r')
                code = autopep8.fix_code(f.read())
                f.close()
                relevant_code_snippets = extract_class_with_imports(
                    source_code = code, class_name = row['Name'].split(".")[-1])
                human_written_code = relevant_code_snippets

                proj_data_list.append(human_written_code)
                skeleton, total_prog_units, total_docstr = (extract_skeleton(human_written_code))
                proj_data_list.append(skeleton)
                proj_data_list.append(total_prog_units)
                proj_data_list.append(total_docstr)
                success_counter += 1
                print(f"Class {row['Name']} -> Successful.")
            except Exception as e:
                print(f"Class {row['Name']} -> Unsuccessful.")
                fail_counter += 1
                fail_log_dict[fail_counter] = (row['repo_name'], row['File'], row['Name'], repr(e))

            if len(proj_data_list) == 8:
                full_data_list.append(proj_data_list)
        subprocess.run(f"rm -rf {path_to_data}/git_repos_for_analysis/{repo_folder}", shell=True)
        successful_process_logger.write(f"{repo},{full_class_df[full_class_df['repo_name'] == repo].shape[0]},{success_counter}\n")
        print(f"{total_counter} classes gone through the extraction process so far.")


    if len(fail_log_dict) > 0:
        error_file = open(f"{path_to_data}/metadata_folder/skeleton_extraction_failures.log", "a")
        for key, value in fail_log_dict.items():
            error_file.write(f"{key}: {value}\n")
        error_file.close()
    successful_process_logger.close()
    return pd.DataFrame(full_data_list, columns = ['repo_name', 'File', 'Name', 'RatioCommentToCode', 'human_written_code', 'code_skeleton',
                                     'total_program_units', 'total_doc_str']).drop_duplicates(subset=['human_written_code'], keep='last')

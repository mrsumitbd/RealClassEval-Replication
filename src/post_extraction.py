import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import warnings, os
warnings.filterwarnings("ignore")
from utility import combine_understand_reports, refine_indentation, total_program_unit_fixer
import ast
import sys
import types

path_to_data = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def post_extraction(full_skeleton_df):
    und_report_df = combine_understand_reports(sys.argv[1])

    full_skeleton_df.dropna(inplace=True)

    merged_df = pd.merge(full_skeleton_df, und_report_df,how='inner', left_on=['repo_name', 'File', 'Name', 'RatioCommentToCode'], 
                     right_on = ['repo_name', 'File', 'Name', 'RatioCommentToCode'])
    
    
    merged_df.dropna(inplace=True, axis=1)

    merged_df.drop(columns=['Kind', 'report_file_name'], inplace=True)

    cols = ['Project', 'File', 'Class_Name', 'RatioCommentToCode',
       'Human_Written_Code', 'Code_Skeleton', 'Total_Program_Units',
       'Total_Docstr', 'AvgCountLine', 'AvgCountLineBlank',
       'AvgCountLineCode', 'AvgCountLineComment', 'AvgCyclomatic',
       'CountClassBase', 'CountClassCoupled', 'CountClassCoupledModified',
       'CountClassDerived', 'CountDeclInstanceMethod',
       'CountDeclInstanceVariable', 'CountDeclMethod', 'CountDeclMethodAll',
       'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl',
       'CountLineCodeExe', 'CountLineComment', 'CountStmt', 'CountStmtDecl',
       'CountStmtExe', 'MaxCyclomatic', 'MaxInheritanceTree', 'MaxNesting',
       'SumCyclomatic']
    merged_df.columns = cols

    # reorder columns
    l = list(range(0,3))

    l.extend(list(range(4,13)))
    l.extend([3])
    l.extend(list(range(13,34)))

    merged_df = merged_df.iloc[:, l]

    merged_df.rename(columns={
        'RatioCommentToCode' : 'CommentToCodeRatio'
    }, inplace=True)

    merged_df.reset_index(inplace=True)

    merged_df['index'] = list(range(0, merged_df.shape[0]))

    merged_df.rename(columns={'index': 'id'}, inplace=True)

    merged_df.rename(columns={
        'Project' : 'repository_name',
        'File' : 'file_path',
        'Class_Name' : 'class_name',
        'Human_Written_Code' : 'human_written_code',
        'Code_Skeleton' : 'class_skeleton', 
        'Total_Program_Units' : 'total_program_units', 
        'Total_Docstr' : 'total_doc_str'
    }, inplace=True)

    merged_df.drop_duplicates(subset=['repository_name', 'file_path', 'class_name'], inplace=True)

    merged_df.reset_index(inplace=True)
    merged_df.drop(columns=['index'], inplace=True)
    merged_df['id'] = list(range(0, merged_df.shape[0]))

    merged_df['class_skeleton'] = [refine_indentation(skeleton) for skeleton in merged_df['class_skeleton'].tolist()]

    merged_df.to_csv(f"{path_to_data}/metadata_folder/{sys.argv[1]}/cleaned_class_skeletons_with_understand_mertics.csv", index=False)

    print(f"Total number of classes after merging with Understand report is {len(merged_df)}")

    return merged_df

def outlier_removal(df):
    count_df = pd.DataFrame(df.repository_name.value_counts(normalize=False))

    perc_10, perc_90 = count_df['count'].quantile([0.1, 0.9]) # keeping only the repos that are within the 10th and 90th percentile
    count_df = count_df[(count_df['count'] >= perc_10) & (count_df['count'] <= perc_90)]

    filtered_projects = count_df.index.tolist()

    return df[df['repository_name'].isin(filtered_projects)].reset_index().drop(columns=['index'])


def is_valid_class(code_str: str) -> bool:
    """
    Checks if the given code string represents a Python class that:
    - Uses only standard libraries or pip-installable libraries.
    - Has no relative imports (e.g., from . or ..).
    - Has no references to undefined (likely internal) artifacts.
    - Contains no async def methods.
    - Contains no wildcard imports (from ... import *).
    """
    # Parse the code to check for syntax errors, async defs, relative imports, and star imports
    try:
        tree = ast.parse(code_str)
    except SyntaxError:
        return False

    # Check for async def
    if any(isinstance(node, ast.AsyncFunctionDef) for node in ast.walk(tree)):
        return False

    # Check for star imports (disallow to avoid ambiguity in mocking)
    if any(
        isinstance(node, ast.ImportFrom) and any(alias.name == '*' for alias in node.names)
        for node in ast.walk(tree)
    ):
        return False

    # Prepare isolated namespace for execution
    namespace = {}
    original_import = __builtins__.__import__

    def mock_import(name, globals=None, locals=None, fromlist=(), level=0):
        if level > 0:
            raise ImportError("Relative import not allowed")
        
        # Try to import normally (for builtins/standard libs)
        try:
            return original_import(name, globals, locals, fromlist, level)
        except ImportError:
            # Mock non-standard (assume pip-installable) modules
            parts = name.split('.')
            mod_name = parts[0]
            if mod_name in sys.modules:
                mod = sys.modules[mod_name]
            else:
                mod = types.ModuleType(mod_name)
                sys.modules[mod_name] = mod
            
            current_mod = mod
            for part in parts[1:]:
                if not hasattr(current_mod, part):
                    sub_mod = types.ModuleType(part)
                    setattr(current_mod, part, sub_mod)
                current_mod = getattr(current_mod, part)
            
            # Handle specific fromlist items with dummies
            if fromlist:
                for item in fromlist:
                    if item != '*':  # * already disallowed
                        if not hasattr(current_mod, item):
                            setattr(current_mod, item, None)  # Dummy value/class/function
            
            return current_mod

    # Set up builtins with mocked import
    builtins_dict = dict(__builtins__.__dict__)
    builtins_dict['__import__'] = mock_import
    mocked_builtins = types.ModuleType('builtins')
    mocked_builtins.__dict__.update(builtins_dict)
    
    namespace['__name__'] = '__main__'
    namespace['__builtins__'] = mocked_builtins

    # Execute the code in the isolated namespace
    try:
        exec(code_str, namespace)
        return True
    except NameError:
        # Undefined name likely indicates internal dependency
        return False
    except ImportError as e:
        # Relative import or other issues
        return False
    except Exception:
        # Any other execution errors (e.g., syntax in exec, though parsed)
        return False
    
def get_solo_testable_classes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the DataFrame to include only classes that are likely solo-testable.
    Criteria:
    - No base classes (CountClassBase == 0)
    - Low coupling (CountClassCoupled <= 5)
    - Moderate complexity (SumCyclomatic <= 25)
    - Valid class structure (passes is_valid_class check)
    - Not a test class (class name or file path contains 'test')
    - Total program units between 3 and median of total_program_units
    """
    filtered_df = df[
        (df['CountClassBase'] == 0) &
        #(df['CountClassCoupled'] <= 5) &
        #(df['SumCyclomatic'] <= 25) &
        df['human_written_code'].apply(is_valid_class) # &
        #(df['total_program_units'] > 3)
    ]

    test_mask = (
        filtered_df['class_name'].str.contains('test|Test', case=False, na=False) |
        filtered_df['file_path'].str.contains('test', case=False, na=False)
    )
    
    filtered_df = filtered_df[~test_mask]

    filtered_df['total_program_units'] = [total_program_unit_fixer(code_snippet) for code_snippet in filtered_df['human_written_code'].tolist()]
    filtered_df = filtered_df[filtered_df.total_program_units.between(3, filtered_df.total_program_units.value_counts().median())]

    return filtered_df


if __name__ == "__main__":
    full_skeleton_df = pd.read_csv(f"{path_to_data}/metadata_folder/{sys.argv[1]}/extracted_class_skeletons-raw_version.csv")
    
    cleaned_skleton_df = outlier_removal(post_extraction(full_skeleton_df))

    final_df = get_solo_testable_classes(cleaned_skleton_df)
    final_df.to_csv(f"{path_to_data}/metadata_folder/{sys.argv[1]}/pynguin_testable_classes.csv", index=False)
    print(f"Final number of classes after all the filtering is {final_df.shape[0]}")

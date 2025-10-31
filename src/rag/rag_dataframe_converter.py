"""
Convert pandas DataFrame with Understand metrics to v1_dataset.json format.
"""

import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFrameToDatasetConverter:
    """Convert DataFrame with code and metrics to v1_dataset.json format."""

    # Known column mappings
    REQUIRED_COLUMNS = {
        'id': 'id',
        'repository_name': 'repository_name',
        'file_path': 'file_path',
        'class_name': 'class_name',
        'human_written_code': 'implementation',
        'class_skeleton': 'skeleton',
        'total_program_units': 'total_program_units',
        'total_doc_str': 'total_doc_str'
    }

    # Common Understand metrics (based on web search)
    # These will be included in metadata if present
    UNDERSTAND_METRICS = [
        # Complexity metrics
        'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe',
        'CountLine', 'CountLineBlank', 'CountLineComment',
        'CountStmt', 'CountStmtDecl', 'CountStmtExe',
        'CountDeclClass', 'CountDeclFunction', 'CountDeclMethod',
        'Cyclomatic', 'CyclomaticModified', 'CyclomaticStrict',
        'Essential', 'MaxNesting',

        # Object-oriented metrics
        'CountClassBase', 'CountClassCoupled', 'CountClassDerived',
        'PercentLackOfCohesion', 'MaxInheritanceTree',

        # Method/Function metrics
        'CountInput', 'CountOutput', 'CountPath',
        'MaxCyclomatic', 'SumCyclomatic',

        # Comment metrics
        'RatioCommentToCode',

        # Other
        'Knots'
    ]

    def __init__(self):
        """Initialize converter."""
        pass

    def convert(self, df: pd.DataFrame,
                output_path: str,
                include_metadata: bool = False,
                custom_metric_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Convert DataFrame to v1_dataset.json format.

        Args:
            df: Input DataFrame with code and metrics
            output_path: Path to save output JSON file
            include_metadata: Whether to include Understand metrics in metadata
            custom_metric_columns: List of custom metric column names to include

        Returns:
            Dictionary with conversion statistics
        """
        logger.info(f"Converting DataFrame with {len(df)} rows")
        logger.info(f"Include metadata: {include_metadata}")

        # Validate DataFrame
        self._validate_dataframe(df)

        # Convert to dataset format
        dataset = []
        skipped = 0

        for idx, row in df.iterrows():
            try:
                item = self._convert_row(row, include_metadata, custom_metric_columns)
                dataset.append(item)
            except Exception as e:
                logger.warning(f"Skipping row {idx}: {e}")
                skipped += 1
                continue

        # Save to JSON
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)

        logger.info(f"Conversion complete:")
        logger.info(f"  - Converted: {len(dataset)} examples")
        logger.info(f"  - Skipped: {skipped} examples")
        logger.info(f"  - Output: {output_path}")

        return {
            'total_rows': len(df),
            'converted': len(dataset),
            'skipped': skipped,
            'output_path': str(output_path)
        }

    def _validate_dataframe(self, df: pd.DataFrame):
        """Validate that DataFrame has required columns."""
        missing_columns = []

        for req_col in self.REQUIRED_COLUMNS.keys():
            if req_col not in df.columns:
                missing_columns.append(req_col)

        if missing_columns:
            raise ValueError(f"DataFrame missing required columns: {missing_columns}")

        logger.info("DataFrame validation passed")

    def _convert_row(self, row: pd.Series,
                    include_metadata: bool,
                    custom_metric_columns: Optional[List[str]]) -> Dict[str, Any]:
        """Convert a single DataFrame row to dataset item."""

        # Basic required fields
        item = {
            'class_name': str(row['class_name']),
            'skeleton': str(row['class_skeleton']),
            'implementation': str(row['human_written_code'])
        }

        # Add metadata if requested
        if include_metadata:
            metadata = self._extract_metadata(row, custom_metric_columns)
            if metadata:
                item['metadata'] = metadata

        return item

    def _extract_metadata(self, row: pd.Series,
                         custom_metric_columns: Optional[List[str]]) -> Dict[str, Any]:
        """Extract metadata from row."""
        metadata = {}

        # Add basic info
        metadata['id'] = str(row['id'])
        metadata['repository_name'] = str(row['repository_name'])
        metadata['file_path'] = str(row['file_path'])
        metadata['total_program_units'] = int(row['total_program_units']) if pd.notna(row['total_program_units']) else 0
        metadata['total_docstr'] = int(row['total_docstr']) if pd.notna(row['total_docstr']) else 0

        # Add Understand metrics
        understand_metrics = {}

        # Check for standard Understand metrics
        for metric in self.UNDERSTAND_METRICS:
            if metric in row.index and pd.notna(row[metric]):
                understand_metrics[metric] = self._convert_metric_value(row[metric])

        # Check for custom metrics
        if custom_metric_columns:
            for metric in custom_metric_columns:
                if metric in row.index and pd.notna(row[metric]):
                    understand_metrics[metric] = self._convert_metric_value(row[metric])

        # Add any other columns that look like metrics (start with Count, Max, Sum, etc.)
        for col in row.index:
            if col not in self.REQUIRED_COLUMNS and col not in understand_metrics:
                if self._looks_like_metric(col) and pd.notna(row[col]):
                    understand_metrics[col] = self._convert_metric_value(row[col])

        if understand_metrics:
            metadata['understand_metrics'] = understand_metrics

        return metadata

    def _looks_like_metric(self, column_name: str) -> bool:
        """Check if column name looks like a metric."""
        metric_prefixes = ['Count', 'Max', 'Min', 'Sum', 'Avg', 'Ratio',
                          'Percent', 'Cyclomatic', 'Essential', 'Knots']
        return any(column_name.startswith(prefix) for prefix in metric_prefixes)

    def _convert_metric_value(self, value) -> Any:
        """Convert metric value to appropriate type."""
        if pd.isna(value):
            return None

        # Try to convert to numeric
        try:
            if isinstance(value, (int, float)):
                return float(value) if '.' in str(value) else int(value)
            return value
        except:
            return str(value)

    def preview_conversion(self, df: pd.DataFrame,
                          num_examples: int = 3,
                          include_metadata: bool = False) -> str:
        """
        Preview what the conversion will look like.

        Args:
            df: Input DataFrame
            num_examples: Number of examples to show
            include_metadata: Whether to include metadata

        Returns:
            JSON string preview
        """
        preview_data = []

        for idx, row in df.head(num_examples).iterrows():
            try:
                item = self._convert_row(row, include_metadata, None)
                preview_data.append(item)
            except Exception as e:
                logger.error(f"Error in row {idx}: {e}")

        return json.dumps(preview_data, indent=2, ensure_ascii=False)

    def get_available_metrics(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Get list of available metrics in the DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            Dictionary with categorized metric names
        """
        all_columns = set(df.columns)
        required = set(self.REQUIRED_COLUMNS.keys())

        # Find potential metric columns
        potential_metrics = all_columns - required

        # Categorize
        found_understand_metrics = []
        other_metrics = []

        for col in potential_metrics:
            if col in self.UNDERSTAND_METRICS:
                found_understand_metrics.append(col)
            elif self._looks_like_metric(col):
                other_metrics.append(col)

        return {
            'understand_metrics': sorted(found_understand_metrics),
            'other_metrics': sorted(other_metrics),
            'total_metrics': len(found_understand_metrics) + len(other_metrics)
        }


def convert_v2_dataframe_to_dataset(df: pd.DataFrame,
                                   output_path: str = "data/v2_dataset.json") -> Dict[str, Any]:
    """
    Convert v2 DataFrame to v2_dataset.json (simpler format, just skeleton + metadata).

    Args:
        df: Input DataFrame with required columns
        output_path: Where to save the JSON file

    Returns:
        Conversion statistics

    Required columns:
        - class_name
        - class_skeleton
        - snippet_id (optional but recommended)

    Example:
        >>> df = pd.read_csv('v2_data.csv')
        >>> stats = convert_v2_dataframe_to_dataset(df, 'data/v2_dataset.json')
    """
    logger.info(f"Converting v2 DataFrame with {len(df)} rows")

    # Check required columns
    required = ['class_name', 'class_skeleton']
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    dataset = []
    for idx, row in df.iterrows():
        item = {
            'class_name': str(row['class_name']),
            'skeleton': str(row['class_skeleton'])
        }

        # Add snippet_id if available
        if 'snippet_id' in df.columns:
            item['snippet_id'] = row['snippet_id']

        dataset.append(item)

    # Save
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    logger.info(f"Converted {len(dataset)} v2 examples to {output_path}")

    return {
        'total_rows': len(df),
        'converted': len(dataset),
        'output_path': str(output_path),
        'has_snippet_id': 'snippet_id' in df.columns
    }


def convert_dataframe_to_dataset(df: pd.DataFrame,
                                output_path: str = "data/v1_dataset.json",
                                include_metadata: bool = False,
                                custom_metrics: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Convenience function to convert DataFrame to v1_dataset.json.

    Args:
        df: Input DataFrame with required columns
        output_path: Where to save the JSON file
        include_metadata: Whether to include Understand metrics in metadata
        custom_metrics: List of additional metric column names to include

    Returns:
        Conversion statistics

    Example:
        >>> df = pd.read_csv('code_data.csv')
        >>> stats = convert_dataframe_to_dataset(
        ...     df,
        ...     output_path='data/v1_dataset.json',
        ...     include_metadata=True
        ... )
        >>> print(f"Converted {stats['converted']} examples")
    """
    converter = DataFrameToDatasetConverter()
    return converter.convert(df, output_path, include_metadata, custom_metrics)


def main():
    """Example usage and testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Convert DataFrame to v1_dataset.json')
    parser.add_argument('--input', required=True, help='Input CSV/Pickle file')
    parser.add_argument('--output', default='data/v1_dataset.json', help='Output JSON file')
    parser.add_argument('--include-metadata', action='store_true', help='Include Understand metrics')
    parser.add_argument('--preview', action='store_true', help='Preview conversion without saving')
    parser.add_argument('--list-metrics', action='store_true', help='List available metrics')
    parser.add_argument('--custom-metrics', nargs='+', help='Additional metric columns to include')

    args = parser.parse_args()

    # Load DataFrame
    logger.info(f"Loading data from {args.input}")
    if args.input.endswith('.csv'):
        df = pd.read_csv(args.input)
    elif args.input.endswith('.pkl') or args.input.endswith('.pickle'):
        df = pd.read_pickle(args.input)
    else:
        raise ValueError("Input must be CSV or Pickle file")

    logger.info(f"Loaded DataFrame with {len(df)} rows and {len(df.columns)} columns")

    converter = DataFrameToDatasetConverter()

    # List metrics if requested
    if args.list_metrics:
        metrics = converter.get_available_metrics(df)
        print("\n" + "="*70)
        print("AVAILABLE METRICS IN DATAFRAME")
        print("="*70)
        print(f"\nUnderstand Metrics Found: {len(metrics['understand_metrics'])}")
        for metric in metrics['understand_metrics']:
            print(f"  - {metric}")
        print(f"\nOther Metrics Found: {len(metrics['other_metrics'])}")
        for metric in metrics['other_metrics'][:20]:  # Show first 20
            print(f"  - {metric}")
        if len(metrics['other_metrics']) > 20:
            print(f"  ... and {len(metrics['other_metrics']) - 20} more")
        print(f"\nTotal Metrics: {metrics['total_metrics']}")
        print("="*70)
        return

    # Preview conversion if requested
    if args.preview:
        print("\n" + "="*70)
        print("CONVERSION PREVIEW (First 3 Examples)")
        print("="*70)
        preview = converter.preview_conversion(df, num_examples=3,
                                              include_metadata=args.include_metadata)
        print(preview)
        print("="*70)
        return

    # Perform conversion
    stats = converter.convert(
        df,
        output_path=args.output,
        include_metadata=args.include_metadata,
        custom_metric_columns=args.custom_metrics
    )

    print("\n" + "="*70)
    print("CONVERSION COMPLETE")
    print("="*70)
    print(f"Total rows processed: {stats['total_rows']}")
    print(f"Successfully converted: {stats['converted']}")
    print(f"Skipped (errors): {stats['skipped']}")
    print(f"Output file: {stats['output_path']}")
    print("="*70)


if __name__ == "__main__":
    main()
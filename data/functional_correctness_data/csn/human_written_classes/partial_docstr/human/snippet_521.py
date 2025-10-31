class AthenaFileFormat:
    """Constants and utilities for Athena supported file formats.

    This class provides constants for file formats supported by Amazon Athena
    and utility methods to check format types. These are commonly used when
    creating tables or configuring UNLOAD operations.

    Supported formats:
        - SEQUENCEFILE: Hadoop SequenceFile format
        - TEXTFILE: Plain text files (default)
        - RCFILE: Record Columnar File format
        - ORC: Optimized Row Columnar format
        - PARQUET: Apache Parquet columnar format
        - AVRO: Apache Avro format
        - ION: Amazon Ion format

    Example:
        >>> from pyathena.model import AthenaFileFormat
        >>>
        >>> # Check if format is Parquet
        >>> if AthenaFileFormat.is_parquet("PARQUET"):
        ...     print("Using columnar format")
        >>>
        >>> # Use in UNLOAD operations
        >>> format_type = AthenaFileFormat.FILE_FORMAT_PARQUET
        >>> sql = f"UNLOAD (...) TO 's3://bucket/path/' WITH (format = '{format_type}')"
        >>> cursor.execute(sql)

    See Also:
        AWS Documentation on supported file formats:
        https://docs.aws.amazon.com/athena/latest/ug/supported-serdes.html
    """
    FILE_FORMAT_SEQUENCEFILE: str = 'SEQUENCEFILE'
    FILE_FORMAT_TEXTFILE: str = 'TEXTFILE'
    FILE_FORMAT_RCFILE: str = 'RCFILE'
    FILE_FORMAT_ORC: str = 'ORC'
    FILE_FORMAT_PARQUET: str = 'PARQUET'
    FILE_FORMAT_AVRO: str = 'AVRO'
    FILE_FORMAT_ION: str = 'ION'

    @staticmethod
    def is_parquet(value: str) -> bool:
        return value.upper() == AthenaFileFormat.FILE_FORMAT_PARQUET

    @staticmethod
    def is_orc(value: str) -> bool:
        return value.upper() == AthenaFileFormat.FILE_FORMAT_ORC
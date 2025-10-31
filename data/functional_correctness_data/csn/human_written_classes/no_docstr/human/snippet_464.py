from typing import Any, Dict, List, Optional, Pattern
import re

class AthenaRowFormatSerde:
    PATTERN_ROW_FORMAT_SERDE: Pattern[str] = re.compile("^(?i:serde) '(?P<serde>.+)'$")
    ROW_FORMAT_SERDE_CSV: str = 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    ROW_FORMAT_SERDE_REGEX: str = 'org.apache.hadoop.hive.serde2.RegexSerDe'
    ROW_FORMAT_SERDE_LAZY_SIMPLE: str = 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
    ROW_FORMAT_SERDE_CLOUD_TRAIL: str = 'com.amazon.emr.hive.serde.CloudTrailSerde'
    ROW_FORMAT_SERDE_GROK: str = 'com.amazonaws.glue.serde.GrokSerDe'
    ROW_FORMAT_SERDE_JSON: str = 'org.openx.data.jsonserde.JsonSerDe'
    ROW_FORMAT_SERDE_JSON_HCATALOG: str = 'org.apache.hive.hcatalog.data.JsonSerDe'
    ROW_FORMAT_SERDE_PARQUET: str = 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
    ROW_FORMAT_SERDE_ORC: str = 'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
    ROW_FORMAT_SERDE_AVRO: str = 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'

    @staticmethod
    def is_parquet(value: str) -> bool:
        match = AthenaRowFormatSerde.PATTERN_ROW_FORMAT_SERDE.search(value)
        if match:
            serde = match.group('serde')
            if serde == AthenaRowFormatSerde.ROW_FORMAT_SERDE_PARQUET:
                return True
        return False

    @staticmethod
    def is_orc(value: str) -> bool:
        match = AthenaRowFormatSerde.PATTERN_ROW_FORMAT_SERDE.search(value)
        if match:
            serde = match.group('serde')
            if serde == AthenaRowFormatSerde.ROW_FORMAT_SERDE_ORC:
                return True
        return False
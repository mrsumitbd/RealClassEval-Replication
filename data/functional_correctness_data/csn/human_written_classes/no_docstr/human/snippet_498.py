class VerticaType:
    UNKNOWN = 4
    BOOL = 5
    INT8 = 6
    FLOAT8 = 7
    CHAR = 8
    VARCHAR = 9
    DATE = 10
    TIME = 11
    TIMESTAMP = 12
    TIMESTAMPTZ = 13
    INTERVAL = 14
    INTERVALYM = 114
    TIMETZ = 15
    NUMERIC = 16
    VARBINARY = 17
    UUID = 20
    LONGVARCHAR = 115
    LONGVARBINARY = 116
    BINARY = 117
    ROW = 300
    ARRAY = 301
    MAP = 302
    ARRAY1D_BOOL = 1505
    ARRAY1D_INT8 = 1506
    ARRAY1D_FLOAT8 = 1507
    ARRAY1D_CHAR = 1508
    ARRAY1D_VARCHAR = 1509
    ARRAY1D_DATE = 1510
    ARRAY1D_TIME = 1511
    ARRAY1D_TIMESTAMP = 1512
    ARRAY1D_TIMESTAMPTZ = 1513
    ARRAY1D_INTERVAL = 1514
    ARRAY1D_INTERVALYM = 1521
    ARRAY1D_TIMETZ = 1515
    ARRAY1D_NUMERIC = 1516
    ARRAY1D_VARBINARY = 1517
    ARRAY1D_UUID = 1520
    ARRAY1D_BINARY = 1522
    ARRAY1D_LONGVARCHAR = 1519
    ARRAY1D_LONGVARBINARY = 1518
    SET_BOOL = 2705
    SET_INT8 = 2706
    SET_FLOAT8 = 2707
    SET_CHAR = 2708
    SET_VARCHAR = 2709
    SET_DATE = 2710
    SET_TIME = 2711
    SET_TIMESTAMP = 2712
    SET_TIMESTAMPTZ = 2713
    SET_INTERVAL = 2714
    SET_INTERVALYM = 2721
    SET_TIMETZ = 2715
    SET_NUMERIC = 2716
    SET_VARBINARY = 2717
    SET_UUID = 2720
    SET_BINARY = 2722
    SET_LONGVARCHAR = 2719
    SET_LONGVARBINARY = 2718

    def __init__(self, *values):
        self.values = values

    def __cmp__(self, other):
        if other in self.values:
            return 0
        if other < self.values:
            return 1
        else:
            return -1

    def __eq__(self, other):
        return other in self.values

    def __ne__(self, other):
        return other not in self.values
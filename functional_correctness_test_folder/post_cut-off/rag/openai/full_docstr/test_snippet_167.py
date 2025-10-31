import pytest
import snippet_167 as module_0

def test_case_0():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    bool_0 = True
    int_0 = 482
    list_0 = [bool_0, int_0, int_0, int_0, int_0]
    packing_metrics_1 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_1).__module__}.{type(packing_metrics_1).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_1.total_sequences == 0
    assert packing_metrics_1.total_bins == 0
    assert packing_metrics_1.total_sequence_length == 0
    assert packing_metrics_1.total_bin_capacity == 0
    assert packing_metrics_1.total_waste == 0
    assert packing_metrics_1.bin_utilizations == []
    assert packing_metrics_1.bin_counts == []
    assert packing_metrics_1.packing_times == []
    assert packing_metrics_1.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    list_1 = []
    dict_0 = packing_metrics_0.update(list_0, list_1, bool_0)
    assert packing_metrics_0.total_sequences == 5
    assert packing_metrics_0.total_sequence_length == 1929
    assert f'{type(packing_metrics_0.bin_utilizations).__module__}.{type(packing_metrics_0.bin_utilizations).__qualname__}' == 'builtins.list'
    assert len(packing_metrics_0.bin_utilizations) == 1
    assert packing_metrics_0.bin_counts == [0]
    assert packing_metrics_0.min_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    packing_metrics_0.get_aggregated_stats()
    packing_metrics_1.get_aggregated_stats()

@pytest.mark.xfail(strict=True)
def test_case_1():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    int_0 = -5405
    packing_metrics_0.update(packing_metrics_0, packing_metrics_0, int_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    list_0 = []
    packing_metrics_0.update(packing_metrics_0, list_0, packing_metrics_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    int_0 = 1731
    int_1 = 3079
    int_2 = 1620
    int_3 = -1581
    list_0 = [int_0, int_1, int_2, int_3]
    list_1 = [list_0]
    packing_metrics_0.calculate_stats_only(packing_metrics_0, list_1, int_3)

@pytest.mark.xfail(strict=True)
def test_case_4():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    list_0 = []
    list_1 = [list_0]
    packing_metrics_0.calculate_stats_only(list_0, list_1, list_1)

def test_case_5():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    packing_metrics_0.print_aggregated_stats()

def test_case_6():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)

def test_case_7():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    bool_0 = False
    packing_metrics_1 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_1).__module__}.{type(packing_metrics_1).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_1.total_sequences == 0
    assert packing_metrics_1.total_bins == 0
    assert packing_metrics_1.total_sequence_length == 0
    assert packing_metrics_1.total_bin_capacity == 0
    assert packing_metrics_1.total_waste == 0
    assert packing_metrics_1.bin_utilizations == []
    assert packing_metrics_1.bin_counts == []
    assert packing_metrics_1.packing_times == []
    assert packing_metrics_1.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    list_0 = []
    dict_0 = packing_metrics_1.update(list_0, list_0, bool_0)
    assert f'{type(packing_metrics_1.bin_utilizations).__module__}.{type(packing_metrics_1.bin_utilizations).__qualname__}' == 'builtins.list'
    assert len(packing_metrics_1.bin_utilizations) == 1
    assert packing_metrics_1.bin_counts == [0]
    assert packing_metrics_1.min_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.min_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    packing_metrics_0.get_aggregated_stats()
    packing_metrics_1.print_aggregated_stats()

@pytest.mark.xfail(strict=True)
def test_case_8():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    packing_metrics_0.print_aggregated_stats()
    bool_0 = True
    packing_metrics_1 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_1).__module__}.{type(packing_metrics_1).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_1.total_sequences == 0
    assert packing_metrics_1.total_bins == 0
    assert packing_metrics_1.total_sequence_length == 0
    assert packing_metrics_1.total_bin_capacity == 0
    assert packing_metrics_1.total_waste == 0
    assert packing_metrics_1.bin_utilizations == []
    assert packing_metrics_1.bin_counts == []
    assert packing_metrics_1.packing_times == []
    assert packing_metrics_1.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    bool_1 = False
    list_0 = [bool_0, bool_1, bool_1, bool_1]
    list_1 = [list_0]
    int_0 = -654
    dict_0 = packing_metrics_1.update(list_0, list_1, bool_0, packing_metrics_1)
    assert packing_metrics_1.total_sequences == 4
    assert packing_metrics_1.total_bins == 1
    assert packing_metrics_1.total_sequence_length == 1
    assert packing_metrics_1.total_bin_capacity == 1
    assert f'{type(packing_metrics_1.bin_utilizations).__module__}.{type(packing_metrics_1.bin_utilizations).__qualname__}' == 'builtins.list'
    assert len(packing_metrics_1.bin_utilizations) == 1
    assert packing_metrics_1.bin_counts == [1]
    assert f'{type(packing_metrics_1.packing_times).__module__}.{type(packing_metrics_1.packing_times).__qualname__}' == 'builtins.list'
    assert len(packing_metrics_1.packing_times) == 1
    assert packing_metrics_1.max_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.min_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    dict_1 = packing_metrics_0.update(list_0, list_1, int_0)
    assert packing_metrics_0.total_sequences == 4
    assert packing_metrics_0.total_bins == 1
    assert packing_metrics_0.total_sequence_length == 1
    assert packing_metrics_0.total_bin_capacity == -654
    assert packing_metrics_0.total_waste == -655
    assert f'{type(packing_metrics_0.bin_utilizations).__module__}.{type(packing_metrics_0.bin_utilizations).__qualname__}' == 'builtins.list'
    assert len(packing_metrics_0.bin_utilizations) == 1
    assert packing_metrics_0.bin_counts == [1]
    assert packing_metrics_0.min_utilization == pytest.approx(-0.0015290519877675841, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(1.0015290519877675, abs=0.01, rel=0.01)
    packing_metrics_1.get_aggregated_stats()

@pytest.mark.xfail(strict=True)
def test_case_9():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    packing_metrics_0.print_aggregated_stats()
    bool_0 = True
    packing_metrics_1 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_1).__module__}.{type(packing_metrics_1).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_1.total_sequences == 0
    assert packing_metrics_1.total_bins == 0
    assert packing_metrics_1.total_sequence_length == 0
    assert packing_metrics_1.total_bin_capacity == 0
    assert packing_metrics_1.total_waste == 0
    assert packing_metrics_1.bin_utilizations == []
    assert packing_metrics_1.bin_counts == []
    assert packing_metrics_1.packing_times == []
    assert packing_metrics_1.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    bool_1 = False
    int_0 = 521
    list_0 = [bool_0, int_0, int_0, int_0]
    list_1 = []
    dict_0 = packing_metrics_1.update(list_0, list_1, bool_0, bool_0)
    assert packing_metrics_1.total_sequences == 4
    assert packing_metrics_1.total_sequence_length == 1564
    assert f'{type(packing_metrics_1.bin_utilizations).__module__}.{type(packing_metrics_1.bin_utilizations).__qualname__}' == 'builtins.list'
    assert len(packing_metrics_1.bin_utilizations) == 1
    assert packing_metrics_1.bin_counts == [0]
    assert packing_metrics_1.packing_times == [True]
    assert packing_metrics_1.min_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.min_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    int_1 = -530
    int_2 = -689
    list_2 = [int_1, int_1, int_2]
    packing_metrics_1.get_aggregated_stats()
    list_3 = [bool_1]
    list_4 = [list_3, list_2]
    packing_metrics_0.calculate_stats_only(list_3, list_4, int_2)

def test_case_10():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    bool_0 = True
    packing_metrics_1 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_1).__module__}.{type(packing_metrics_1).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_1.total_sequences == 0
    assert packing_metrics_1.total_bins == 0
    assert packing_metrics_1.total_sequence_length == 0
    assert packing_metrics_1.total_bin_capacity == 0
    assert packing_metrics_1.total_waste == 0
    assert packing_metrics_1.bin_utilizations == []
    assert packing_metrics_1.bin_counts == []
    assert packing_metrics_1.packing_times == []
    assert packing_metrics_1.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_1.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    bool_1 = False
    packing_metrics_1.get_aggregated_stats()
    list_0 = [bool_0, bool_1, bool_1, bool_1]
    list_1 = [list_0, list_0]
    int_0 = -654
    dict_0 = packing_metrics_0.update(list_0, list_1, int_0)
    assert packing_metrics_0.total_sequences == 4
    assert packing_metrics_0.total_bins == 2
    assert packing_metrics_0.total_sequence_length == 1
    assert packing_metrics_0.total_bin_capacity == -1308
    assert packing_metrics_0.total_waste == -1309
    assert f'{type(packing_metrics_0.bin_utilizations).__module__}.{type(packing_metrics_0.bin_utilizations).__qualname__}' == 'builtins.list'
    assert len(packing_metrics_0.bin_utilizations) == 1
    assert packing_metrics_0.bin_counts == [2]
    assert packing_metrics_0.min_utilization == pytest.approx(-0.0007645259938837921, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(1.0007645259938838, abs=0.01, rel=0.01)
    int_1 = -689
    packing_metrics_0.print_aggregated_stats()
    list_2 = [bool_1]
    list_3 = [list_2]
    packing_metrics_0.calculate_stats_only(list_2, list_3, int_1)

@pytest.mark.xfail(strict=True)
def test_case_11():
    packing_metrics_0 = module_0.PackingMetrics()
    assert f'{type(packing_metrics_0).__module__}.{type(packing_metrics_0).__qualname__}' == 'snippet_167.PackingMetrics'
    assert packing_metrics_0.total_sequences == 0
    assert packing_metrics_0.total_bins == 0
    assert packing_metrics_0.total_sequence_length == 0
    assert packing_metrics_0.total_bin_capacity == 0
    assert packing_metrics_0.total_waste == 0
    assert packing_metrics_0.bin_utilizations == []
    assert packing_metrics_0.bin_counts == []
    assert packing_metrics_0.packing_times == []
    assert packing_metrics_0.min_utilization == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.max_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    packing_metrics_0.print_aggregated_stats()
    bool_0 = True
    bool_1 = False
    bool_2 = True
    list_0 = [bool_2, bool_1]
    list_1 = []
    bool_3 = False
    dict_0 = packing_metrics_0.update(list_0, list_1, bool_3, bool_1)
    assert packing_metrics_0.total_sequences == 2
    assert packing_metrics_0.total_sequence_length == 1
    assert f'{type(packing_metrics_0.bin_utilizations).__module__}.{type(packing_metrics_0.bin_utilizations).__qualname__}' == 'builtins.list'
    assert len(packing_metrics_0.bin_utilizations) == 1
    assert packing_metrics_0.bin_counts == [0]
    assert packing_metrics_0.packing_times == [False]
    assert packing_metrics_0.min_utilization == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert packing_metrics_0.min_waste_ratio == pytest.approx(0.0, abs=0.01, rel=0.01)
    int_0 = 521
    list_2 = [bool_0, int_0, int_0, int_0]
    list_3 = []
    dict_1 = packing_metrics_0.update(list_2, list_3, bool_0)
    assert packing_metrics_0.total_sequences == 6
    assert packing_metrics_0.total_sequence_length == 1565
    assert len(packing_metrics_0.bin_utilizations) == 2
    assert packing_metrics_0.bin_counts == [0, 0]
    int_1 = -530
    int_2 = -689
    list_4 = [int_1, int_1, int_2]
    packing_metrics_0.print_aggregated_stats()
    list_5 = [bool_1]
    list_6 = [list_5, list_4]
    packing_metrics_0.calculate_stats_only(list_5, list_6, int_2)
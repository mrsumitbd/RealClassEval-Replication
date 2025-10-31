import pytest
import snippet_97 as module_0

def test_case_0():
    g_c_p_regions_0 = module_0.GCPRegions()
    g_c_p_regions_0.tier1()
    g_c_p_regions_0.tier2()

def test_case_1():
    g_c_p_regions_0 = module_0.GCPRegions()
    g_c_p_regions_0.tier2()

@pytest.mark.xfail(strict=True)
def test_case_2():
    g_c_p_regions_0 = module_0.GCPRegions()
    g_c_p_regions_0.tier2()
    int_0 = -1192
    bool_0 = True
    g_c_p_regions_0.lowest_latency(int_0, g_c_p_regions_0, attempts=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    g_c_p_regions_0 = module_0.GCPRegions()
    g_c_p_regions_0.tier2()
    g_c_p_regions_0.lowest_latency()

@pytest.mark.xfail(strict=True)
def test_case_4():
    none_type_0 = None
    g_c_p_regions_0 = module_0.GCPRegions()
    g_c_p_regions_0.lowest_latency(tier=g_c_p_regions_0, attempts=none_type_0)
    g_c_p_regions_0.tier2()
    g_c_p_regions_0.lowest_latency(verbose=none_type_0)

def test_case_5():
    module_0.GCPRegions()

@pytest.mark.xfail(strict=True)
def test_case_6():
    g_c_p_regions_0 = module_0.GCPRegions()
    g_c_p_regions_1 = module_0.GCPRegions()
    g_c_p_regions_1.tier2()
    g_c_p_regions_0.tier1()
    g_c_p_regions_2 = module_0.GCPRegions()
    bool_0 = True
    g_c_p_regions_2.lowest_latency(bool_0, tier=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    g_c_p_regions_0 = module_0.GCPRegions()
    g_c_p_regions_0.tier2()
    int_0 = -1192
    bool_0 = False
    g_c_p_regions_0.lowest_latency(int_0, g_c_p_regions_0, attempts=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_8():
    int_0 = -1587
    g_c_p_regions_0 = module_0.GCPRegions()
    g_c_p_regions_0.tier1()
    list_0 = g_c_p_regions_0.tier2()
    g_c_p_regions_0.lowest_latency(verbose=int_0, tier=list_0)
    bool_0 = True
    g_c_p_regions_0.lowest_latency(bool_0)
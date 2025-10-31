import decimal as module_0
import snippet_150 as module_1

def test_case_0():
    decimal_0 = module_0.Decimal()
    assert f'{type(decimal_0).__module__}.{type(decimal_0).__qualname__}' == 'decimal.Decimal'
    assert f'{type(module_0.DefaultContext).__module__}.{type(module_0.DefaultContext).__qualname__}' == 'decimal.Context'
    assert module_0.HAVE_CONTEXTVAR is True
    assert module_0.HAVE_THREADS is True
    assert f'{type(module_0.BasicContext).__module__}.{type(module_0.BasicContext).__qualname__}' == 'decimal.Context'
    assert f'{type(module_0.ExtendedContext).__module__}.{type(module_0.ExtendedContext).__qualname__}' == 'decimal.Context'
    assert module_0.MAX_PREC == 999999999999999999
    assert module_0.MAX_EMAX == 999999999999999999
    assert module_0.MIN_EMIN == -999999999999999999
    assert module_0.MIN_ETINY == -1999999999999999997
    assert module_0.ROUND_UP == 'ROUND_UP'
    assert module_0.ROUND_DOWN == 'ROUND_DOWN'
    assert module_0.ROUND_CEILING == 'ROUND_CEILING'
    assert module_0.ROUND_FLOOR == 'ROUND_FLOOR'
    assert module_0.ROUND_HALF_UP == 'ROUND_HALF_UP'
    assert module_0.ROUND_HALF_DOWN == 'ROUND_HALF_DOWN'
    assert module_0.ROUND_HALF_EVEN == 'ROUND_HALF_EVEN'
    assert module_0.ROUND_05UP == 'ROUND_05UP'
    assert f'{type(module_0.Decimal.real).__module__}.{type(module_0.Decimal.real).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_0.Decimal.imag).__module__}.{type(module_0.Decimal.imag).__qualname__}' == 'builtins.getset_descriptor'
    none_type_0 = None
    str_0 = 'Cuj\\FJ0dE({'
    dict_0 = {}
    int_0 = -501
    budget_tracker_0 = module_1.BudgetTracker(none_type_0, decimal_0, decimal_0, dict_0, int_0, decimal_0)
    assert f'{type(budget_tracker_0).__module__}.{type(budget_tracker_0).__qualname__}' == 'snippet_150.BudgetTracker'
    assert budget_tracker_0.initial_budget is None
    assert f'{type(budget_tracker_0.current_balance).__module__}.{type(budget_tracker_0.current_balance).__qualname__}' == 'decimal.Decimal'
    assert f'{type(budget_tracker_0.total_spent).__module__}.{type(budget_tracker_0.total_spent).__qualname__}' == 'decimal.Decimal'
    assert budget_tracker_0.spending_per_agent_card == {}
    assert budget_tracker_0.evaluations_count == -501
    assert f'{type(budget_tracker_0.average_cost_per_eval).__module__}.{type(budget_tracker_0.average_cost_per_eval).__qualname__}' == 'decimal.Decimal'
    none_type_1 = budget_tracker_0.spend(decimal_0, str_0)
    assert f'{type(budget_tracker_0.spending_per_agent_card).__module__}.{type(budget_tracker_0.spending_per_agent_card).__qualname__}' == 'builtins.dict'
    assert len(budget_tracker_0.spending_per_agent_card) == 1
    assert budget_tracker_0.evaluations_count == -500
    bool_0 = budget_tracker_0.can_afford(decimal_0)
    assert bool_0 is True

def test_case_1():
    decimal_0 = module_0.Decimal()
    assert f'{type(decimal_0).__module__}.{type(decimal_0).__qualname__}' == 'decimal.Decimal'
    assert f'{type(module_0.DefaultContext).__module__}.{type(module_0.DefaultContext).__qualname__}' == 'decimal.Context'
    assert module_0.HAVE_CONTEXTVAR is True
    assert module_0.HAVE_THREADS is True
    assert f'{type(module_0.BasicContext).__module__}.{type(module_0.BasicContext).__qualname__}' == 'decimal.Context'
    assert f'{type(module_0.ExtendedContext).__module__}.{type(module_0.ExtendedContext).__qualname__}' == 'decimal.Context'
    assert module_0.MAX_PREC == 999999999999999999
    assert module_0.MAX_EMAX == 999999999999999999
    assert module_0.MIN_EMIN == -999999999999999999
    assert module_0.MIN_ETINY == -1999999999999999997
    assert module_0.ROUND_UP == 'ROUND_UP'
    assert module_0.ROUND_DOWN == 'ROUND_DOWN'
    assert module_0.ROUND_CEILING == 'ROUND_CEILING'
    assert module_0.ROUND_FLOOR == 'ROUND_FLOOR'
    assert module_0.ROUND_HALF_UP == 'ROUND_HALF_UP'
    assert module_0.ROUND_HALF_DOWN == 'ROUND_HALF_DOWN'
    assert module_0.ROUND_HALF_EVEN == 'ROUND_HALF_EVEN'
    assert module_0.ROUND_05UP == 'ROUND_05UP'
    assert f'{type(module_0.Decimal.real).__module__}.{type(module_0.Decimal.real).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_0.Decimal.imag).__module__}.{type(module_0.Decimal.imag).__qualname__}' == 'builtins.getset_descriptor'

def test_case_2():
    decimal_0 = module_0.Decimal()
    assert f'{type(decimal_0).__module__}.{type(decimal_0).__qualname__}' == 'decimal.Decimal'
    assert f'{type(module_0.DefaultContext).__module__}.{type(module_0.DefaultContext).__qualname__}' == 'decimal.Context'
    assert module_0.HAVE_CONTEXTVAR is True
    assert module_0.HAVE_THREADS is True
    assert f'{type(module_0.BasicContext).__module__}.{type(module_0.BasicContext).__qualname__}' == 'decimal.Context'
    assert f'{type(module_0.ExtendedContext).__module__}.{type(module_0.ExtendedContext).__qualname__}' == 'decimal.Context'
    assert module_0.MAX_PREC == 999999999999999999
    assert module_0.MAX_EMAX == 999999999999999999
    assert module_0.MIN_EMIN == -999999999999999999
    assert module_0.MIN_ETINY == -1999999999999999997
    assert module_0.ROUND_UP == 'ROUND_UP'
    assert module_0.ROUND_DOWN == 'ROUND_DOWN'
    assert module_0.ROUND_CEILING == 'ROUND_CEILING'
    assert module_0.ROUND_FLOOR == 'ROUND_FLOOR'
    assert module_0.ROUND_HALF_UP == 'ROUND_HALF_UP'
    assert module_0.ROUND_HALF_DOWN == 'ROUND_HALF_DOWN'
    assert module_0.ROUND_HALF_EVEN == 'ROUND_HALF_EVEN'
    assert module_0.ROUND_05UP == 'ROUND_05UP'
    assert f'{type(module_0.Decimal.real).__module__}.{type(module_0.Decimal.real).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_0.Decimal.imag).__module__}.{type(module_0.Decimal.imag).__qualname__}' == 'builtins.getset_descriptor'
    none_type_0 = None
    str_0 = 'Cuj\\FJ0dE({'
    dict_0 = {}
    int_0 = -501
    budget_tracker_0 = module_1.BudgetTracker(none_type_0, decimal_0, decimal_0, dict_0, int_0, decimal_0)
    assert f'{type(budget_tracker_0).__module__}.{type(budget_tracker_0).__qualname__}' == 'snippet_150.BudgetTracker'
    assert budget_tracker_0.initial_budget is None
    assert f'{type(budget_tracker_0.current_balance).__module__}.{type(budget_tracker_0.current_balance).__qualname__}' == 'decimal.Decimal'
    assert f'{type(budget_tracker_0.total_spent).__module__}.{type(budget_tracker_0.total_spent).__qualname__}' == 'decimal.Decimal'
    assert budget_tracker_0.spending_per_agent_card == {}
    assert budget_tracker_0.evaluations_count == -501
    assert f'{type(budget_tracker_0.average_cost_per_eval).__module__}.{type(budget_tracker_0.average_cost_per_eval).__qualname__}' == 'decimal.Decimal'
    none_type_1 = budget_tracker_0.spend(decimal_0, str_0)
    assert f'{type(budget_tracker_0.spending_per_agent_card).__module__}.{type(budget_tracker_0.spending_per_agent_card).__qualname__}' == 'builtins.dict'
    assert len(budget_tracker_0.spending_per_agent_card) == 1
    assert budget_tracker_0.evaluations_count == -500

def test_case_3():
    decimal_0 = module_0.Decimal()
    assert f'{type(decimal_0).__module__}.{type(decimal_0).__qualname__}' == 'decimal.Decimal'
    assert f'{type(module_0.DefaultContext).__module__}.{type(module_0.DefaultContext).__qualname__}' == 'decimal.Context'
    assert module_0.HAVE_CONTEXTVAR is True
    assert module_0.HAVE_THREADS is True
    assert f'{type(module_0.BasicContext).__module__}.{type(module_0.BasicContext).__qualname__}' == 'decimal.Context'
    assert f'{type(module_0.ExtendedContext).__module__}.{type(module_0.ExtendedContext).__qualname__}' == 'decimal.Context'
    assert module_0.MAX_PREC == 999999999999999999
    assert module_0.MAX_EMAX == 999999999999999999
    assert module_0.MIN_EMIN == -999999999999999999
    assert module_0.MIN_ETINY == -1999999999999999997
    assert module_0.ROUND_UP == 'ROUND_UP'
    assert module_0.ROUND_DOWN == 'ROUND_DOWN'
    assert module_0.ROUND_CEILING == 'ROUND_CEILING'
    assert module_0.ROUND_FLOOR == 'ROUND_FLOOR'
    assert module_0.ROUND_HALF_UP == 'ROUND_HALF_UP'
    assert module_0.ROUND_HALF_DOWN == 'ROUND_HALF_DOWN'
    assert module_0.ROUND_HALF_EVEN == 'ROUND_HALF_EVEN'
    assert module_0.ROUND_05UP == 'ROUND_05UP'
    assert f'{type(module_0.Decimal.real).__module__}.{type(module_0.Decimal.real).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_0.Decimal.imag).__module__}.{type(module_0.Decimal.imag).__qualname__}' == 'builtins.getset_descriptor'
    none_type_0 = None
    bool_0 = False
    str_0 = "'Qg6,X1^+@k+=IPo$Q"
    dict_0 = {str_0: decimal_0, str_0: decimal_0}
    budget_tracker_0 = module_1.BudgetTracker(bool_0, decimal_0, decimal_0, dict_0, bool_0, decimal_0)
    assert f'{type(budget_tracker_0).__module__}.{type(budget_tracker_0).__qualname__}' == 'snippet_150.BudgetTracker'
    assert budget_tracker_0.initial_budget is False
    assert f'{type(budget_tracker_0.current_balance).__module__}.{type(budget_tracker_0.current_balance).__qualname__}' == 'decimal.Decimal'
    assert f'{type(budget_tracker_0.total_spent).__module__}.{type(budget_tracker_0.total_spent).__qualname__}' == 'decimal.Decimal'
    assert f'{type(budget_tracker_0.spending_per_agent_card).__module__}.{type(budget_tracker_0.spending_per_agent_card).__qualname__}' == 'builtins.dict'
    assert len(budget_tracker_0.spending_per_agent_card) == 1
    assert budget_tracker_0.evaluations_count is False
    assert f'{type(budget_tracker_0.average_cost_per_eval).__module__}.{type(budget_tracker_0.average_cost_per_eval).__qualname__}' == 'decimal.Decimal'
    var_0 = budget_tracker_0.__eq__(none_type_0)
    dict_1 = {}
    budget_tracker_1 = module_1.BudgetTracker(none_type_0, decimal_0, decimal_0, dict_1, bool_0, decimal_0)
    assert f'{type(budget_tracker_1).__module__}.{type(budget_tracker_1).__qualname__}' == 'snippet_150.BudgetTracker'
    assert budget_tracker_1.initial_budget is None
    assert f'{type(budget_tracker_1.current_balance).__module__}.{type(budget_tracker_1.current_balance).__qualname__}' == 'decimal.Decimal'
    assert f'{type(budget_tracker_1.total_spent).__module__}.{type(budget_tracker_1.total_spent).__qualname__}' == 'decimal.Decimal'
    assert budget_tracker_1.spending_per_agent_card == {}
    assert budget_tracker_1.evaluations_count is False
    assert f'{type(budget_tracker_1.average_cost_per_eval).__module__}.{type(budget_tracker_1.average_cost_per_eval).__qualname__}' == 'decimal.Decimal'
    none_type_1 = budget_tracker_1.spend(decimal_0, var_0)
    assert f'{type(budget_tracker_1.spending_per_agent_card).__module__}.{type(budget_tracker_1.spending_per_agent_card).__qualname__}' == 'builtins.dict'
    assert len(budget_tracker_1.spending_per_agent_card) == 1
    assert budget_tracker_1.evaluations_count == 1
    bool_1 = budget_tracker_1.can_afford(decimal_0)
    assert bool_1 is True
import pytest
# import pandas as pd
from src.nypd import func


@pytest.mark.parametrize("yr, dflt, common, res", [(1, 2, {1}, 1), (1, 2, {0}, 2), (1, 2, {1, 2}, 1)])
def test_yr_or_default(yr, dflt, common, res):
    assert func.yr_or_default(yr, dflt, common) == res


@pytest.mark.parametrize("start, end, gdp, population, co2, non_year_colnames, res_gdp, res_pop, res_co2",
                         [(1, 2, )])
def test_selected_yrs_dfs(start, end, gdp, population, co2, non_year_colnames, res_gdp, res_pop, res_co2):
    assert func.selected_yrs_dfs(start, end, gdp, population, co2, non_year_colnames) == res

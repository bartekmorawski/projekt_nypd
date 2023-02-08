import pytest
import pandas as pd
from src.nypd import func


@pytest.mark.parametrize("yr, dflt, common, res", [(1, 2, {1}, 1), (1, 2, {0}, 2), (1, 2, {1, 2}, 1)])
def test_yr_or_default(yr, dflt, common, res):
    assert func.yr_or_default(yr, dflt, common) == res


df_gdp = pd.DataFrame({"clmn": ["row1", "row2"], "1": ["a", "b"], "2": ["c", "d"], "3": ["e", "f"], "rmv": [1, 2]})
df_pop = pd.DataFrame({"clmn": ["row3", "row4"], "1": ["a1", "b1"], "2": ["c", "d"], "3": ["e1", "f1"], "rmv": [1, 2]})
df_co2 = pd.DataFrame({"Year": [0, 1, 2, 3], "co2_clmn": [8, 9, 3, 10]})
df_res_gdp = pd.DataFrame({"clmn": ["row1", "row2"], "1": ["a", "b"], "2": ["c", "d"]})
df_res_pop = pd.DataFrame({"clmn": ["row3", "row4"], "1": ["a1", "b1"], "2": ["c", "d"]})
df_res_co2 = pd.DataFrame({'Year': [1, 2], "co2_clmn": [9, 3]})


@pytest.mark.parametrize("start, end, gdp, population, co2, non_year_colnames, res_gdp, res_pop, res_co2",
                         [(1, 2, df_gdp, df_pop, df_co2, ['clmn'], df_res_gdp, df_res_pop, df_res_co2)])
def test_selected_yrs_dfs(start, end, gdp, population, co2, non_year_colnames, res_gdp, res_pop, res_co2):
    [res_gdp_t, res_pop_t, res_co2_t] = func.selected_yrs_dfs(start, end, gdp, population, co2, non_year_colnames)
    print(df_res_co2)
    assert df_res_gdp.equals(res_gdp_t)
    assert df_res_pop.equals(res_pop_t)
    assert df_res_co2.equals(res_co2_t.reset_index(drop=True))


df_co2_top = pd.DataFrame({"Year": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                           "Country": ["PL", "GB", "US", "FR", "SE", "HR", "PL", "GB", "US", "FR", "SE", "HR"],
                           "Per Capita": [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 0],
                           "Total": [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]})
df_co2_top_res = pd.DataFrame({"Year": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                               "Country": ["GB", "US", "FR", "SE", "HR", "PL", "GB", "US", "FR", "SE"],
                               "Per Capita": [2, 3, 4, 5, 6, 1, 2, 3, 4, 5],
                               "Total": [9, 9, 9, 9, 9, 9, 9, 9, 9, 9]})


@pytest.mark.parametrize("co2_par, res_co2", [(df_co2_top, df_co2_top_res)])
def test_top_5_co2_by_year(co2_par, res_co2):
    jp = func.top_5_co2_by_year(co2_par)
    assert jp.equals(res_co2)

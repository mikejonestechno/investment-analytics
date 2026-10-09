import pandas as pd
import pytest

from data_loader import parse_rba_dates


def test_parses_slash_day_month_year():
    # G1 (and F5 2024-25) format, day first: 01/02/1959 must be 1 Feb, not 2 Jan
    dates = parse_rba_dates(pd.Series(['31/01/1959', '01/02/1959']))
    assert list(dates) == [pd.Timestamp('1959-01-31'), pd.Timestamp('1959-02-01')]


def test_parses_dash_day_month_name_year():
    # F5 format from 2026
    dates = parse_rba_dates(pd.Series(['31-Jan-1959', '28-Feb-1959', '30-Sep-2026']))
    assert list(dates) == [pd.Timestamp('1959-01-31'), pd.Timestamp('1959-02-28'), pd.Timestamp('2026-09-30')]


def test_parses_month_year_as_month_end():
    # format used until 2023
    dates = parse_rba_dates(pd.Series(['Jan-1959', 'Jun-1922']))
    assert list(dates) == [pd.Timestamp('1959-01-31'), pd.Timestamp('1922-06-30')]


def test_keeps_index():
    dates = parse_rba_dates(pd.Series(['31-Jan-1959'], index=[11]))
    assert list(dates.index) == [11]


@pytest.mark.parametrize('bad', ['1959-01-31', '31/13/1959', 'Series ID', ''])
def test_rejects_unknown_format(bad):
    with pytest.raises(ValueError, match='Unrecognised RBA date format'):
        parse_rba_dates(pd.Series(['31-Jan-1959', bad]))

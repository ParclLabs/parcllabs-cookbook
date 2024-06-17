import pandas as pd
import numpy as np


class TimeSeriesAnalysis:
    def __init__(self, df, date_col, value_col, freq='D'):
        self.df = df.copy()
        self.date_col = date_col
        self.value_col = value_col
        self.freq = freq
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        self.df = self.df.sort_values(by=date_col)

    def calculate_changes(self, change_since_date=None):
        if self.freq == 'D':
            intervals = {
                '24_hour': pd.DateOffset(days=1),
                '7_day': pd.DateOffset(days=7),
                '1_month': pd.DateOffset(months=1),
                '3_month': pd.DateOffset(months=3),
                '6_month': pd.DateOffset(months=6),
                '12_month': pd.DateOffset(years=1),
                '2_year': pd.DateOffset(years=2),
                '5_year': pd.DateOffset(years=5),
                '10_year': pd.DateOffset(years=10)
            }
        elif self.freq == 'M':
            intervals = {
                '1_month': pd.DateOffset(months=1),
                '3_month': pd.DateOffset(months=3),
                '6_month': pd.DateOffset(months=6),
                '12_month': pd.DateOffset(years=1),
                '2_year': pd.DateOffset(years=2),
                '5_year': pd.DateOffset(years=5),
                '10_year': pd.DateOffset(years=10)
            }
        else:
            raise ValueError("Unsupported frequency. Use 'D' for daily or 'M' for monthly.")

        results = {}

        current_value = self.df[self.value_col].iloc[-1]
        current_date = self.df[self.date_col].iloc[-1]

        for key, offset in intervals.items():
            past_date = current_date - offset
            past_df = self.df[self.df[self.date_col] <= past_date]

            if not past_df.empty:
                past_value = past_df[self.value_col].iloc[-1]
                percent_change = round((current_value - past_value) / past_value, 4)
                results[key] = float(percent_change)  # Convert to native Python float

        # Calculate peak_to_current
        max_value = self.df[self.value_col].max()
        max_date = self.df[self.df[self.value_col] == max_value][self.date_col].iloc[0]
        peak_to_current_change = round((current_value - max_value) / max_value, 4)
        series_max_date = self.df[self.date_col].max().date().isoformat()

        results['peak_to_current'] = {
            'percent_change': float(peak_to_current_change),  # Convert to native Python float
            'peak_date': max_date.date().isoformat(),
            'peak_value': float(max_value)  # Convert to native Python float
        }

        results['series_max_date'] = series_max_date

        # Calculate change_since_date if provided
        if change_since_date is not None:
            change_since_date = pd.to_datetime(change_since_date)
            if self.freq == 'M':
                change_since_date = change_since_date.to_period('M').to_timestamp()

            since_date_df = self.df[self.df[self.date_col] <= change_since_date]
            if not since_date_df.empty:
                since_date_value = since_date_df[self.value_col].iloc[-1]
                since_date_change = round((current_value - since_date_value) / since_date_value, 4)
                results['change_since_date'] = {
                    'percent_change': float(since_date_change),  # Convert to native Python float
                    'change_date': change_since_date.date().isoformat(),
                    'change_value': float(since_date_value)  # Convert to native Python float
                }

        return results

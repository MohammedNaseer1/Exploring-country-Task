import sqlite3
import pandas as pd

DB_PATH = "wdi.sqlite"

country_df = pd.read_csv("Country.csv")
indicators_df = pd.read_csv("Indicators.csv")

conn = sqlite3.connect(DB_PATH)

country_df.to_sql("Country", conn, if_exists="replace", index=False)
indicators_df.to_sql("Indicators", conn, if_exists="replace", index=False)

print("Database built successfully with tables: Country, Indicators")

def run_query(query, params=None):
    return pd.read_sql_query(query, conn, params=params)
highest_gdp_2014 = run_query("""
    SELECT CountryName, Value
    FROM Indicators
    WHERE IndicatorName = 'GDP per capita (current US$)'
      AND Year = 2014
    ORDER BY Value DESC
    LIMIT 1;
""")
print(highest_gdp_2014)
ranked_gdp_2014 = run_query("""
    SELECT CountryName, Value
    FROM Indicators
    WHERE IndicatorName = 'GDP per capita (current US$)'
      AND Year = 2014
    ORDER BY Value DESC;
""")
print(ranked_gdp_2014.head(10))
avg_gdp_per_country = run_query("""
    SELECT CountryName, AVG(Value) AS avg_gdp_per_capita
    FROM Indicators
    WHERE IndicatorName = 'GDP per capita (current US$)'
    GROUP BY CountryName
    ORDER BY avg_gdp_per_capita DESC;
""")
print(avg_gdp_per_country.head(10))

avg_gdp_selected = run_query("""
    SELECT CountryName, AVG(Value) AS avg_gdp_per_capita
    FROM Indicators
    WHERE IndicatorName = 'GDP per capita (current US$)'
      AND CountryName IN ('Brazil', 'China', 'India')
    GROUP BY CountryName
    ORDER BY avg_gdp_per_capita DESC;
""")
print(avg_gdp_selected)
max_year = run_query("SELECT MAX(Year) AS max_year FROM Indicators;")["max_year"][0]
start_year = max_year - 9

measures_last_10y = run_query("""
    SELECT COUNT(*) AS n_measures
    FROM Indicators
    WHERE Year BETWEEN ? AND ?;
""", params=(start_year, max_year))
print(f"Between {start_year} and {max_year}:")
print(measures_last_10y)

measures_per_year = run_query("""
    SELECT Year, COUNT(*) AS n_measures
    FROM Indicators
    WHERE Year BETWEEN ? AND ?
    GROUP BY Year
    ORDER BY Year;
""", params=(start_year, max_year))
print(measures_per_year)
measures_per_country = run_query("""
    SELECT CountryName, COUNT(*) AS n_measures
    FROM Indicators
    GROUP BY CountryName
    ORDER BY n_measures ASC;
""")
print(measures_per_country.head(10))

angola_measures = run_query("""
    SELECT CountryName, COUNT(*) AS n_measures
    FROM Indicators
    WHERE CountryName = 'Angola'
    GROUP BY CountryName;
""")
print(angola_measures)

angola_by_year = run_query("""
    SELECT Year, COUNT(*) AS n_measures
    FROM Indicators
    WHERE CountryName = 'Angola'
    GROUP BY Year
    ORDER BY Year;
""")
print(angola_by_year)
tables = run_query("SELECT name FROM sqlite_master WHERE type='table';")
print(tables)
brazil_gdp_2014_join = run_query("""
    SELECT
        i.CountryName,
        i.CountryCode,
        i.IndicatorName,
        i.IndicatorCode,
        i.Year,
        i.Value,
        c.Region,
        c.IncomeGroup
    FROM Indicators AS i
    JOIN Country AS c
        ON i.CountryCode = c.CountryCode
    WHERE i.CountryName = 'Brazil'
      AND i.Year = 2014
      AND i.IndicatorName LIKE '%GDP%'
    ORDER BY i.IndicatorName;
""")
print(brazil_gdp_2014_join)
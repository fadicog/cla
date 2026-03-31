import pandas as pd
import numpy as np

# Read the Excel file
file_path = r'D:\cluade\6.4.0WeeklyTrend.xlsx'
xl_file = pd.ExcelFile(file_path)

print('='*80)
print('EXCEL FILE ANALYSIS: 6.4.0WeeklyTrend.xlsx')
print('='*80)
print(f'\nSheet Names: {xl_file.sheet_names}')
print(f'Number of Sheets: {len(xl_file.sheet_names)}\n')

# Analyze each sheet
for sheet_name in xl_file.sheet_names:
    print('='*80)
    print(f'SHEET: {sheet_name}')
    print('='*80)

    df = pd.read_excel(xl_file, sheet_name=sheet_name)

    print(f'\nShape: {df.shape[0]} rows x {df.shape[1]} columns')
    print(f'\nColumn Names:')
    for i, col in enumerate(df.columns, 1):
        print(f'  {i}. {col}')

    print(f'\nData Types:')
    print(df.dtypes)

    print(f'\nFirst 10 rows:')
    print(df.head(10))

    print(f'\nLast 5 rows:')
    print(df.tail(5))

    print(f'\nBasic Statistics:')
    print(df.describe())

    print(f'\nMissing Values:')
    print(df.isnull().sum())

    print('\n')

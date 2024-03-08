import pandas as pd

df = pd.read_excel(r'C:\Users\Administrator\Desktop\aliexpress\sunyou.xlsx', sheet_name='Sheet2')
for y in range(20, 101, 20):
    print(y)
    df1 = df['logistics_number'][:y].values
    x = ''
    for i in df1:
        i = i + '\n'
        x = x + i
    logist_number_group = x
    print(logist_number_group)
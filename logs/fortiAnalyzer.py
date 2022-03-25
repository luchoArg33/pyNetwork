import pandas as pd
# 18: dest interface
# 20: dest IP
# 21: dest port
# 50: source interface
# 52: source IP
# Sometimes Fortianalyzer imports more or less csv data (I don't know why). This means you will have
# different column indexes for the data you want to retrieve. Adapt the script to your situation
# Use read_csv('logs2.csv') and print(df.columns) to retrieve information about your data

pd.options.display.width = 0                                                                        # Display all columns
pd.set_option('display.max_rows', None)                                                             # Display all rows
df = pd.read_csv('log_file.csv', usecols=[18, 20, 21, 50, 52], low_memory=False, header=None)
result = df.groupby([50, 18, 21, 20]).size()
print(result)

import scipy.io as io
import pandas as pd
import numpy as np

file_name_path = "/home/baiy4/ScanDL/scripts/data/zuco/task1/Raw data/ZAB/ZAB_SR1_ET.mat"
file_name = file_name_path.split('.')[0].split('/')[-1]

mat_data = io.loadmat(file_name_path, squeeze_me=True, struct_as_record=False)

# Print all top-level keys and their structure
print("Top-level keys in the .mat file:")
for key in mat_data.keys():
    if not key.startswith('__'):  # Skip metadata keys
        val = mat_data[key]
        print(f"\nKey: {key}")
        print(f"Type: {type(val)}")
        # If it's an array, print its shape
        if isinstance(val, np.ndarray):
            print(f"Shape: {val.shape}")
            # If not too large, print a small sample
            if val.size < 50:
                print("Data sample:", val)
        else:
            # For non-ndarray types, just print the value or part of it
            # (Be careful with large data.)
            print("Value:", val)

# Extract the colheader and data
colheader = mat_data['colheader']
data = mat_data['data']

print("\n\n--- Detailed Info for colheader & data ---")
print("colheader:", colheader)
print("colheader Type:", type(colheader))
print("colheader Shape:", getattr(colheader, 'shape', None))

# Determine column names
if isinstance(colheader, str):
    column_names = [colheader]
elif hasattr(colheader, 'ndim') and colheader.ndim == 2:
    flattened = colheader[0]
    column_names = []
    for c in flattened:
        if isinstance(c, (list, np.ndarray)) and len(c) > 0:
            column_names.append(str(c[0]))
        else:
            column_names.append(str(c))
else:
    column_names = list(colheader)

print("Column Names:", column_names)

print("data Type:", type(data))
print("data Shape:", data.shape)

# A small sample of the data (first few rows)
print("Data sample (first 5 rows):")
print(data[:5, :])

# Create the DataFrame
df = pd.DataFrame(data, columns=column_names)

output_csv = f"/home/baiy4/ScanDL/scripts/data/zuco/raw_data/{file_name}.csv"
df.to_csv(output_csv, index=False)
print(f"Data saved to {output_csv}")

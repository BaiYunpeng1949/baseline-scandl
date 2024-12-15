import os
from utils_ZuCo import *

# instantiate data transformer object for task 1 (corresponds to the folder where results for task 1 in specified subdir are stored) on sentence level with min-max scaling
datatransform_t1 = DataTransformer('task1', level='sentence', scaling='min-max', fillna='zeros')

# NOTE: data for each sbj will be stored in a pd.DataFrame (i.e., this is a list of 12 pd.DataFrames)
sbjs_t1 = [datatransform_t1(i) for i in range(12)]

# show the first couple of rows for subject 1 for task 1
sbjs_t1[0].head()

# convert DataFrame to .csv file and save it to path
path = os.path.join('zuco', 'processed_data', 'subject1.csv')       # TODO need to change the save path
if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path), exist_ok=True)
sbjs_t1[0].to_csv(path)
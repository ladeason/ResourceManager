import joblib
import numpy as np
import os
import time
import psutil
import pandas as pd
import warnings
from sklearn.utils.validation import _check_sample_weight

warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn.utils.validation')

def get_runq_sz():
    """retusn processes in run que"""
    try:
        with open('/proc/loadavg', 'r') as f:
            return int(float(f.read().split()[3].split('/')[0]))
    except Exception as e:
        return f"Error: {e}"
def get_plist_sz():
    """returns the total number of processes in the system"""
    return len(psutil.pids())
def get_load_avg():
    """returns system load averages (1, 5, 15 minutes)"""
    return os.getloadavg()

# Load the trained model and scaler
clf = joblib.load('svm_model.pkl')
scaler = joblib.load('scaler.pkl')

# Specify feature columns
feature_columns = ['runq_sz', 'plist_sz', 'ldavg_1', 'ldavg_5', 'ldavg_15']  # Replace with actual column names

# Function to take user input and make a prediction
def predict_input(interval=1):
    """continuously monitors and prints system metrics in real time"""
    print(f"{'TIME':<10}{'RUNQ-SZ':<10}{'PLIST-SZ':<10}")
    try: 
        #print("runq_sz    plist_sz   ldavg_1  ldavg_5  ldavg_15   prediction")
        print(f"{'runq_sz':<10}{'plist_sz':<11}{'ldavg_1':<10}{'ldavg_5':<10}{'ldavg_15':<11}{'prediction'}")
        while True:
            runq_sz = get_runq_sz()
            plist_sz = get_plist_sz()
            ldavg_1, ldavg_5, ldavg_15 = get_load_avg()

            pred_data = [[runq_sz, plist_sz, ldavg_1, ldavg_5, ldavg_15]]
            #input_df = pd.DataFrame(pred_data, columns= feature_columns)
            input_array = scaler.transform(pred_data)
            #input_array = scaler.transform(input_df)
            prediction = clf.predict(input_array)
            #print(f'Input values: {pred_data}')
            #print(f"{runq_sz}    {plist_sz}   {ldavg_1}  {ldavg_5}  {ldavg_15}   {prediction[0]}")
            print(f"{runq_sz:<10}{plist_sz:<11}{ldavg_1:<10.4f}{ldavg_5:<10.4f}{ldavg_15:<11.4f}{prediction[0]}")
            #print(f'Predicted label: {prediction[0]}')
            yield{
                "runq_sz":runq_sz,
                "plist_sz":plist_sz,
                "ldavg_1":ldavg_1,
                "ldavg_5":ldavg_5,
                "ldavg_15":ldavg_15,
                "prediction":prediction
            }
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n Monitoring stopped")
    

# Run input prediction
predict_input()

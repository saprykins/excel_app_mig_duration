# improvements: 
# not all dates were mentioned though mig duration was available
# some durations were negative
# manual manipulations still required: 
# a/ i get duration for the last 7 days updates apps, 
# b/ i delete duplicates, 
# c/ i add id for lines, 
# d/  calc app duration, 
# e/ manual cleaning



import csv
from datetime import datetime


# Read the CSV data
filename = './results/ADO_MS_duration_extract_22-290523.csv'  # Replace with the actual filename
# filename = './results/ADO_MS_duration_extract_15-220523.csv'  # Replace with the actual filename
output_filename = './results/apps_durations.csv'  # Replace with the desired output filename


# Define the start and end task prefixes
start_task_prefix = 'TA50.10.'
end_task_prefix = 'TA50.40.'

# Initialize a dictionary to store the process durations for each application
process_durations = {}

# Read the CSV file
with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Iterate over the rows
    for row in reader:
        app_id = row['App id']
        app_name = row['App name']
        task_name = row['Task']
        start_time = row['Start time']
        end_time = row['End time']
        
        # Check if the task name starts with the specified prefixes
        if task_name.startswith(start_task_prefix):
            if app_name not in process_durations:
                process_durations[app_name] = {'app_id': app_id, 'start_time': start_time, 'end_time': None}
            else:
                if process_durations[app_name]['start_time'] is not None:
                    process_durations[app_name]['start_time'] = min(process_durations[app_name]['start_time'], start_time)
                else:
                    process_durations[app_name]['start_time'] = start_time
                    
        elif task_name.startswith(end_task_prefix):
            if app_name not in process_durations:
                process_durations[app_name] = {'app_id': app_id, 'start_time': None, 'end_time': end_time}
            else:
                if process_durations[app_name]['end_time'] is not None:
                    process_durations[app_name]['end_time'] = max(process_durations[app_name]['end_time'], end_time)
                else:
                    process_durations[app_name]['end_time'] = end_time

# Calculate the durations for each application
for app_name, durations in process_durations.items():
    if durations['start_time']:
        start_time = datetime.strptime(durations['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        mig_date = start_time.strftime('%Y-%m-%d')  # Extract the date from the start time
        process_durations[app_name]['mig_date'] = mig_date
    else:
        process_durations[app_name]['mig_date'] = None
    
    if durations['end_time']:
        end_time = datetime.strptime(durations['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        end_time = None
    
    if start_time and end_time:
        duration = end_time - start_time
        process_durations[app_name]['duration'] = duration.total_seconds() / 60
    else:
        process_durations[app_name]['duration'] = None

# Write the results to a CSV file
# output_filename = 'process_durations.csv'  # Replace with the desired output filename

with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['App ID', 'App Name', 'Mig Date', 'Duration (min)'])
    for app_name, durations in process_durations.items():
        writer.writerow([durations['app_id'], app_name, durations['mig_date'], durations['duration']])

print("Process durations have been calculated and saved to", output_filename)

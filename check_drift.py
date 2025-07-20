import pandas as pd, json, sys
try:
    from evidently.report import Report
    from evidently.metrics import DatasetDriftMetric
except ModuleNotFoundError:
    print('Evidently not installed → exiting 0.')
    sys.exit(0)

ref   = pd.read_parquet('data/reference.parquet')
batch = pd.read_parquet('data/latest_batch.parquet')

rep = Report(metrics=[DatasetDriftMetric()])
rep.run(reference_data=ref, current_data=batch)
result = rep.as_dict()
json.dump(result, open('drift.json','w'))
sys.exit(1 if result['metrics'][0]['result']['dataset_drift'] else 0)

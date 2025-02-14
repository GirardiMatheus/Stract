import csv
from io import StringIO

def generate_csv(data, headers):
    output = StringIO()
    
    if "account_name" in headers:
        headers.remove("account_name") 
        headers = ["account_name"] + headers  
    
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    return output.getvalue()

def aggregate_data(data, group_by, numeric_fields):
    aggregated = {}
    for item in data:
        key = item[group_by]
        if key not in aggregated:
            aggregated[key] = {field: 0 for field in numeric_fields}
            aggregated[key][group_by] = key
        for field in numeric_fields:
            aggregated[key][field] += item.get(field, 0)
    return list(aggregated.values())
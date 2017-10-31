import sys
from collections import defaultdict
import csv
from datetime import datetime
from statistics import median

def valid_date(trx_date):
    try:
        datetime.strptime(trx_date, '%m%d%Y')
    except ValueError:
        return False
    else:
        return True

def read_input(filename, cols, cols_relevant):
    with open(filename) as f:
        for line in f:
            data = line.split('|')
            row = {k:v.strip() for k,v in zip(cols, data)}
            if not row['OTHER_ID']:
                if row['CMTE_ID'] and row['TRANSACTION_AMT']:
                    row_filtered = {k:v for k,v in row.items() if k in cols_relevant}
                    yield row_filtered

def parse_input(filename, cols, cols_relevant, cols_by_zip, cols_by_date):
    total_amt_by_zip = {}
    trx_amt_by_zip = defaultdict(list)
    median_amt_by_zip = {}
    count_trx_by_zip = {}
    aggregated_by_zip_sublist = []
    aggregated_by_zip_list = []
    total_amt_by_date = {}
    trx_amt_by_date = defaultdict(list)
    median_amt_by_date = {}
    count_trx_by_date = {}
    aggregated_by_date_dict = defaultdict(list)


    for row in read_input(filename, cols, cols_relevant):
        if len(row['ZIP_CODE']) >= 5:
            row['ZIP_CODE'] = row['ZIP_CODE'][:5]
            key = tuple(row[c] for c in cols_by_zip)
            count_trx_by_zip[key] = count_trx_by_zip.setdefault(key, 0) + 1
            total_amt_by_zip[key] = total_amt_by_zip.setdefault(key, 0) + float(row['TRANSACTION_AMT'])
            trx_amt_by_zip[key].append(float(row['TRANSACTION_AMT']))
            median_amt_by_zip[key] = median(trx_amt_by_zip[key])
            aggregated_by_zip_sublist = [row[c] for c in cols_by_zip]
            aggregated_by_zip_sublist.extend([round(median_amt_by_zip[key]),count_trx_by_zip[key],round(total_amt_by_zip[key])])
            aggregated_by_zip_list.append(aggregated_by_zip_sublist)

        if valid_date(row['TRANSACTION_DT']):
            key = tuple(row[c] for c in cols_by_date)
            count_trx_by_date[key] = count_trx_by_date.setdefault(key, 0) + 1
            total_amt_by_date[key] = total_amt_by_date.setdefault(key, 0) + float(row['TRANSACTION_AMT'])
            trx_amt_by_date[key].append(float(row['TRANSACTION_AMT']))
            median_amt_by_date[key] = median(trx_amt_by_date[key])

    for d in (median_amt_by_date, count_trx_by_date, total_amt_by_date):
        for k, v in d.items():
            aggregated_by_date_dict[k].append(v)

    aggregated_by_date_dict = {k:[round(e) if isinstance(e, float) else e for e in v] for k,v in aggregated_by_date_dict.items()}

    return (aggregated_by_zip_list, aggregated_by_date_dict)


if __name__ == '__main__':
    cols = ['CMTE_ID', 'col2','col3','col4','col5','col6','col7','col8','col9', 'col10', 'ZIP_CODE', 'col12','col13', 'TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID', 'col17', 'col18', 'col19', 'col20', 'col21', 'col22']
    cols_relevant = ['CMTE_ID','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT']
    cols_by_zip = ['CMTE_ID', 'ZIP_CODE']
    cols_by_date = ['CMTE_ID', 'TRANSACTION_DT']

    aggregated_by_zip_list, aggregated_by_date_dict  = parse_input(sys.argv[1], cols, cols_relevant, cols_by_zip, cols_by_date)

    with  open(sys.argv[2],'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')
        for item in aggregated_by_zip_list:
            writer.writerow([item[0], item[1], item[2], item[3], item[4]])

    with  open(sys.argv[3],'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')
        for k,v in sorted(aggregated_by_date_dict.items()):
            *key, = k
            writer.writerow(key + v)

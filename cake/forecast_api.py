from datetime import datetime

import sys
import os
print(os.getcwd())
import boto3
import DynamoInterractor 
#import DynamoDB

sys.path.insert(1, '/app/ML')
sys.path.insert(1, '/var/lib/docker/volumes/ML/_data/ML')
import Forecast
import Cluster
import best_pairs


def get(request):

    is_cached = True #djangoSettings.CACHE
    if type(request) != dict:
        request_data = request.data.dict()
    else: 
        request_data = request
    action = request_data.get("action")
    date_from = request_data.get("from")
    date_to = request_data.get("to")
    shop = request_data.get("shop")
    branch = request_data.get("branch")

    shop += '/'

    identifier = shop + '-' + branch + '-' + action + ':' + date_from + '/' + date_to
    identifier = {'identifier': identifier}
    identifier.update({'from': date_from})

    DynamoInterractor.DynamoDB.connect_db()
    DynamoInterractor.DynamoDB.connect_or_create_table()
    #results['step_3'] = DynamoDB.put_data(request_data)
    candidate = DynamoInterractor.DynamoDB.get_data(identifier)
    #print(candidate)

    if (not 'Item' in candidate) or (not is_cached):

        if action == 'pairs':
            json_to_send = best_pairsapi_send(branch, date_from, date_to)

        if action == 'forecast':
            forecast_to_send = Forecast.form_data(Shop_name = shop)
            json_to_send = {'json': {'history': forecast_to_send[0], 'forecast': forecast_to_send[1]}}

        if action == 'cluster':
            #attention, floating point values are stored as strings in DynamoDB!!!
            pair_to_send  = Cluster.return_df_week(branch, date_from, date_to)             
            json_to_send = {'json': {'pie': pair_to_send[0], 'graph': pair_to_send[1]}}

        if (not 'Item' in candidate):

            json_to_send.update(identifier)
            DynamoInterractor.DynamoDB.put_data(json_to_send)

    else:

        json_to_send = candidate['Item']


Today = datetime.now().strftime("%Y-%m-%d")

for Shop_name in ['Bachmann', 'Wolf']:
    
    print( Shop_name, Today)
    payload = {'action': 'forecast',
    'from': Today,
    'to': Today,
    'branch': '1',
    'shop': Shop_name}

    get(payload)

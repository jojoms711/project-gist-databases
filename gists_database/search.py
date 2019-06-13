from .models import Gist
from datetime import datetime
"""
def search_gists(db_connection, **kwargs):
    query = 'Select * from gists'
    if not kwargs:
        cursor = db_connection.execute(query)
        
    else:
        #if there are multiple where clauses
        query += ' where '
        #kwargs is a dict {k:v,k2:v2, ....}
        clause = ''
        comparisons = {
            '__lte': '<=', 
           '__gte' :'>=', 
            '__lt' : '<',
            '__gt' : '>'
        }

        for k, v in kwargs.items(): 
            if isinstance(v, datetime):
                if '__' not in k:
                    operator = '='
                else:
                    for c_key, c_value in comparisons.items():
                        if c_key in k:
                            operator = c_value
                            #rename key eg. created_at__lte as created_at
                            pos = k.find('__')
                            k = k[:pos]
                k= str('datetime({})'.format(k))
                v= str(v) 
                
            else: #if no datetime comparison
                operator = '='
            q = "'"
            clause += k+ operator + q +v +q + ' AND '
            
        clause = clause.rstrip(' AND ')
        query += clause   
        
        cursor = db_connection.execute(query)
    
    ################    
    results = [Gist(row) for row in cursor]
    return results  
"""
    

def comparison(operator):
    return {
        'lt': '<',
        'lte': '<=',
        'gt': '>',
        'gte': '>=',
    }[operator]

def search_gists(db_connection, **kwargs):


#     if 'github_id' in kwargs:
#         cursor = db_connection.execute('SELECT * FROM gists WHERE github_id = :github_id', kwargs)
#         return [Gist(gist) for gist in cursor]
# #         return cursor.fetchall()
#     if 'created_at' in kwargs:
#         cursor = db_connection.execute('SELECT * FROM gists WHERE datetime(created_at) == datetime(:created_at)', kwargs)
#         return [Gist(gist) for gist in cursor]
# #         return cursor.fetchall()
#     else:
#         cursor = db_connection.execute('SELECT * FROM gists')
#         return cursor.fetchall()

    query = 'SELECT * FROM gists'
    params = {}
    if kwargs:
        filters = []
        for param, value in kwargs.items():
            if param.startswith(('created_at', 'updated_at')):
                if '__' in param:
                    attribute, operator = param.split('__')
                    oper = comparison(operator)
                    filters.append('datetime({}) {} datetime(:{})'.format(attribute, oper, param))

                else:
                    attribute = param
                    filters.append('datetime({}) == datetime(:{})'.format(attribute, param))
                params[param] = value

            else:
                filters.append('%s = :%s' % (param, param))
                params[param] = value

        query += ' WHERE '
        query += ' AND '.join(filters)
        cursor = db_connection.execute(query, params)
    else:
        cursor = db_connection.execute(query)

    results = [Gist(gist) for gist in cursor]
    return results  
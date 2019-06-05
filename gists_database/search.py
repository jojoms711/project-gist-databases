from .models import Gist
import datetime

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
            if type(v) == datetime.datetime:
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
     
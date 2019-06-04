import requests,sqlite3


def import_gists_to_database(db, username, commit=True):
    
    #1 - raise GET request 
    url = 'https://api.github.com/users/{}/gists'.format(username)
    resp = requests.get(url)
    resp.raise_for_status() #throws error with details if resp.ok = false
    gist_dict = resp.json()
    

    #2 - create insert query template --- table name is hardcoded as gists according to test file
    Insert_query = """
    INSERT INTO gists(
    'github_id', 'html_url', 'git_pull_url', 'git_push_url', 
    'commits_url', 'forks_url', 'public', 'created_at', 
    'updated_at', 'comments', 'comments_url'
    ) VALUES (
    :github_id, :html_url, :git_pull_url, :git_push_url, 
    :commits_url, :forks_url, :public, :created_at,
    :updated_at, :comments, :comments_url
    );
    """ 
    
    #3 - insert data into table
    for gist in gist_dict:
        params ={
            'github_id' : gist['id'],
            'html_url': gist['html_url'],
            'git_pull_url' : gist['git_pull_url'],
            'git_push_url':gist['git_push_url'],
            'commits_url' :gist['commits_url'],
            'forks_url':gist['forks_url'],
            'public':gist['public'],
            'created_at' :gist['created_at'],
           'updated_at':gist['updated_at'],
            'comments' : gist['comments'],
            'comments_url': gist['comments_url']
            }
        db.execute(Insert_query,params)
        if commit:
            db.commit()
#https://api.github.com/users/{username}/gists


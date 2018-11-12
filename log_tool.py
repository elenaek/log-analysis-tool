import psycopg2
import bleach


DBNAME = "news"


db = psycopg2.connect(database=DBNAME)


def getMostPopularArticles(num):
    query = '''    
        select a.slug, count(path) as views
        from articles a, log l
        where a.slug = replace(l.path, '/article/','')
        group by a.slug
        order by views desc
        limit %s
    '''
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute(query, (str(num), ))
    results = cursor.fetchall()
    db.close()
    return results


def getMostPopularAuthors(num):
    query = '''    
        select au.name, count(l.path) as views
        from articles a, log l, authors au
        where a.slug = replace (l.path, '/article/','') and a.author = au.id
        group by au.name
        order by views desc
        limit %s
    '''
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute(query, (str(num), ))
    results = cursor.fetchall()
    db.close()
    return results

def getErrors(percent):
    query = '''    
        select cast(er.errors as float)/cast(tr.total_requests as float)*100 as error_percentage, er.day
        from errors_per_day er, requests_per_day tr
        where er.day = tr.day AND cast(er.errors as float)/cast(tr.total_requests as float)*100 > %s
    '''
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute(query, (str(percent), ))
    results = cursor.fetchall()
    db.close()
    return results

print(getMostPopularArticles(3))
print(getMostPopularAuthors(10))
print(getErrors(1))
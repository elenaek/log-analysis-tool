#!/usr/bin/env python3

import psycopg2
import bleach


DBNAME = "news"


db = psycopg2.connect(database=DBNAME)


def getMostPopularArticles(num):
    query = '''    
        select a.title, count(path) as views
        from articles a, log l
        where a.slug = replace(l.path, '/article/','')
        group by a.title
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


def outputFormattedAnswer(numArticles, numAuthors, percentErrors):
    print("Get three most popular articles: ")
    for article in getMostPopularArticles(numArticles):
        print('{title} - {viewcount} views'.format(title=article[0], viewcount=article[1]))
    print("\n")

    print("Get authors listed by most popular: ")
    for author in getMostPopularAuthors(numAuthors):
        print('{author} - {viewcount} views'.format(author=author[0], viewcount=author[1]))
    print("\n")

    print("List days where more than 1% of requests are errors: ".format())
    for day in getErrors(percentErrors):
        print("{date:%B} {date:%d}, {date:%Y} - {error_percentage}% errors".format(date=day[1], error_percentage=float(round(day[0], 2))))


outputFormattedAnswer(3,10,1)

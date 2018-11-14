#!/usr/bin/env python3


# Import modules
import psycopg2

# Name of database
DBNAME = "news"


# Function that returns the most popular articles,
# rows limited by numArticles parameter,
# in descending order (Most popular first)
def getMostPopularArticles(numArticles):
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
    cursor.execute(query, (str(numArticles), ))
    results = cursor.fetchall()
    db.close()
    return results


# Function that returns the most popular
# authors (based on view aggregates of their articles),
# rows limited by numAuthors parameter,
# in descending order (Most popular first)
def getMostPopularAuthors(numAuthors):
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
    cursor.execute(query, (str(numAuthors), ))
    results = cursor.fetchall()
    db.close()
    return results


# Function that retrives the days where the percentage of errors exceed the
# percent parameter and outputs the date and percentage of errors that day
def getErrors(percentErrors):
    query = '''
        select cast(er.errors as float)/cast(tr.total_requests as float)*100 as error_percentage, er.day
        from errors_per_day er, requests_per_day tr
        where er.day = tr.day AND cast(er.errors as float)/cast(tr.total_requests as float)*100 > %s
    '''
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute(query, (str(percentErrors), ))
    results = cursor.fetchall()
    db.close()
    return results


# Function that outputs a report, formatted to match the project criteria
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


# Calls outputFormattedAnswer and feeds it the parameters to output the properly formatted results based on project criteria:
# Most popular 3 articles and authors listed in descending order. Days where request errors exceed 1%
outputFormattedAnswer(3, 10, 1)

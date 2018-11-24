#!/usr/bin/env python3

import psycopg2
from datetime import datetime

'''
code used to output list to .txt file (lines 32-34, 62-64, 94-96) taken from
Stack Overflow:
https://stackoverflow.com/questions/899103/writing-a-list-to-a-file-with-python
'''


# question 1
def most_popular_articles():
    '''Returns 3 most popular articles, most popular at the top'''
    question = "1. What are the most popular three articles of all time?"
    query = '''select articles.title, count(articles.time) as page_views
                from articles
                join log on articles.slug = (select substring(path, '[^/]*$'))
                where log.status = '200 OK'
                group by articles.title
                order by page_views desc
                limit 3;
                '''
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    titles = [x[0] for x in results]
    page_views = [x[1] for x in results]
    c.close()

    # outputting results of query to text file
    output = []
    for title, page_view in zip(titles, page_views):
        output.append("{} - {} views".format(title, page_view))
    with open("question1.txt", "w") as f:
        f.write(question + "\n\r")
        f.write("\n".join(output))


# question 2
def most_popular_authors():
    '''Returns most popular author in sorted list based on page views'''
    question = "2. Who are the most popular article authors of all time?"
    query = '''select authors.name, sum(article_pageviews.page_views)
               as total_pageviews
               from articles
               join authors on articles.author = authors.id
               join article_pageviews on
               articles.title = article_pageviews.title
               group by authors.name
               order by total_pageviews desc;
               '''
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    authors = [x[0] for x in results]
    page_views = [x[1] for x in results]
    c.close()

    # outputting results of query to text file
    output = []
    for author, page_view in zip(authors, page_views):
        output.append("{} - {} views".format(author, page_view))
    with open("question2.txt", "w") as f:
        f.write(question + "\n\r")
        f.write("\n".join(output))


# question 3
def find_error_rate():
    '''Returns date and error percentage on days where percentage > 1.00'''
    question = "3. On which days did more than 1% of requests lead to errors?"
    query = '''select data.day as day, round(100.0 * sum(err)/sum(att),2)
                as err_pct
                from (
                        select date(time) as day, count(*) as att, sum(case
                        when status = '404 NOT FOUND' then 1 else 0 end) as err
                        from log
                        group by date(time)
                        ) as data
                group by data.day, data.err, data.att
                having round(100.0 * sum(err)/sum(att),3) > 1.00;
                '''
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    dates = [datetime.strftime(x[0], '%B %d, %Y') for x in results]
    pcts = [x[1] for x in results]
    c.close()

    # outputting results of query to text file:
    output = []
    for date, pct in zip(dates, pcts):
        output.append("{} - {}% error rate".format(date, pct))
    with open("question3.txt", "w") as f:
        f.write(question + "\n\r")
        f.write("\n".join(output))


most_popular_articles()
most_popular_authors()
find_error_rate()

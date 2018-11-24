# News Report
News Report is a tool that uses SQL and Python to query a database and return
the most popular articles, authors, as well as error rates for requests to the
newspaper's website.

## Get The Data
Download the data here: [NEWS][6166d444]

  [6166d444]: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip "Newspaper Data"

## Installation
Ensure the Vagrant VirtualBox is installed. Save the downloaded data in the vagrant directory that along with the virtual machine. Load the data with the following command:
**<p align=center>psql -d news -f newsdata.sql</p>**

## Usage
The script connects to the database via the Python module **psycopg2**. The line below is an example of how to connect:
**<p align=center>db = psycopg2.connect("dbname=news")</p>**
The script also uses the **datetime** module to help format the date value that is returned from the database.

The query used in the second scenario makes use of a view created from the data in the Article table titled **article_pageviews**
It can be created with the following SQL statement:
  > CREATE VIEW article_pageviews AS<br>
  > SELECT articles.title, count(articles.time) AS page_views<br>
  > FROM articles<br>
  > JOIN log ON articles.slug = ((SELECT substring(log.path, '[^/]*$') AS "substring"))
  > WHERE log.status = '200 OK'<br>
  > GROUP BY articles.title;

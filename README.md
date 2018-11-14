# Getting Started


### Preface

This guide assumes you already have:

- The Vagrant VM up and functional with PSQL and python
- You are on the Vagrant VM's console using `vagrant ssh`
- You have cloned this repo into your own directory

### Import the mock database/data using PSQL

Run this command in the directory that contains newsdata.sql: `psql -d news -f newsdata.sql` 

This will create a database called `news` with some mock data.

### Create these views in PSQL

```
psql news
```

```sql
create view errors_per_day as select count(status) as errors, cast(time as date) as day
  from log
  where status = '404 NOT FOUND'
  group by day
  order by day asc;
```

```sql
create view requests_per_day as select count(status) as total_requests, cast(time as date) as day
  from log
  group by day
  order by day asc;
```

### Run the python tool

`python log_tool.py`

This command will generate the reports as output in the console.




# Tool Design

### Database System

This tool uses the `psycopg2` module to query a **PSQL** database `news` in order to generate reports.

### Query Functions
 
 `getMostPopularArticles(numArticles)`: returns a list of tuples with the most popular articles sorted by descending order. The output contains article title and the number of times that article has been viewed.
 
 Parameter: `numArticles` determines how many articles are returned.
 
 `getMostPopularAuthors(numAuthors)`: returns a list of tuples with the most popular authors determined by the aggregate sum of views from articles they have written. The output contains author name and their total views summed from all their articles. Sorted by descending order.
 
 Parameter: `numAuthors` determines how many authors are returned.
 
 `def getErrors(percentErrors)`: returns a list of tuples with the days where the amount of errors exceeds the `percentErrors` parameter. The output contains the date and the % of errors that day.
 
 Parameter: `percentErrors` determines the threshold for reporting dates. When the number of errors in a given day crosses the percentage passed here, that day will be added to the output.
 
 `outputFormattedAnswer(numArticles, numAuthors, percentErrors)`: Utilizes all of the previous functions to generate an output report via `print()` formatted in the way the project requests.

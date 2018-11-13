# Getting Started

## Create these views


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

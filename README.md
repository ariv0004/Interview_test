Retail Bank Demo Data

# Task 1

For the first question is about the Import the CRM events and CRM call centre logs tables into a PostgreSQL database. Use
SQL to join the tables and summarise the average time to resolve complaints across a number of different dimensions.

using PostGresSQL by join the table and calculate the average in a minutes and the we group by based on the issues.


## Below is the sql code
select avg(extract(second from ser_time) + extract(minute from ser_time) * 60 + extract(hour from ser_time)* 3600)/60 as minutes, e.issue
    from crm_call_center_logs c inner join crm_events e on c.complaint_id = e.complaint_id
    group by e.issue;


# Task 2

Import the Luxury Loan Portfolio into pandas dataframes and use Plotly dash to create a web app that displays 3 charts of different types that show interesting business metrics.

- Firstly we will plot using barchart the Total Funded Amount based on Need in every years we can see that the total is very different for every year and needs
- Second is the map of new yorkers payment based on Building Class Category by find the coordinate and create a map
- Third is Box plot load balance based on employment length we will see that is there any connection between the year of experience and load balance.

using this filter we will create a dashboard using dash.

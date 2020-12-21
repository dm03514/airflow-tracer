# airflow-tracer
Trace airflow dag executions

Tracing is replacement for the gantt chart. It shows the duration and result of each individual
task instance within the context of a single dag run. This is a POC for a github issue:

https://github.com/apache/airflow/issues/12771


- Start Airflow, Postgres and Jaeger

```
$ docker-compose up -d
```

- Navigate to the airflow UI and invoke a dag


- Connect to postgres and get a dagrun associated with the dag

```
$ psql -U airflow -h localhost
Password for user airflow:
psql (12.4, server 9.6.20)
Type "help" for help.

airflow=#
```


- Install requirements

```
$ pip install -r requirements.txt
```

- Build the trace. The second parameter is the value that you copied from the database. Make sure to set the timezone to `+00:00`.
```
$ AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@localhost/airflow python cmd/trace-dag-run.py example_bash_operator '2020-12-20 20:17:44.157211+00:00'
```

- Navigate to the jaeger UI to view the trace

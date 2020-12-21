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

<img width="1675" alt="Screen Shot 2020-12-20 at 8 01 04 PM" src="https://user-images.githubusercontent.com/321963/102729323-4f084300-42fe-11eb-82f3-e48eeccaa97d.png">

- Connect to postgres and get a dagrun associated with the dag

```
$ psql -U airflow -h localhost
Password for user airflow:
psql (12.4, server 9.6.20)
Type "help" for help.

airflow=#
```

<img width="1663" alt="Screen Shot 2020-12-20 at 8 04 02 PM" src="https://user-images.githubusercontent.com/321963/102729404-a4dceb00-42fe-11eb-9a0e-84d9c257718f.png">


- Install requirements

```
$ pip install -r requirements.txt
```

- Build the trace. The second parameter is the value that you copied from the database. Make sure to set the timezone to `+00:00`.
```
$ AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@localhost/airflow python cmd/trace-dag-run.py example_bash_operator '2020-12-20 20:17:44.157211+00:00'
```

- Navigate to the jaeger UI to view the trace

<img width="1680" alt="Screen Shot 2020-12-20 at 8 07 32 PM" src="https://user-images.githubusercontent.com/321963/102729518-043afb00-42ff-11eb-9a33-58a5f4d5ba5f.png">


--- 
Tracing provides a similiar view as the airfflow "Gantt" chart:

<img width="1680" alt="Screen Shot 2020-12-20 at 8 24 49 PM" src="https://user-images.githubusercontent.com/321963/102730117-73b1ea00-4301-11eb-87a5-3d17d9c961bb.png">

<img width="1680" alt="Screen Shot 2020-12-20 at 8 25 54 PM" src="https://user-images.githubusercontent.com/321963/102730158-9fcd6b00-4301-11eb-92e9-1f33f5a7a371.png">


# airflow-tracer
Trace airflow dag executions

```
$ AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@localhost/airflow python cmd/trace-dag-run.py example_bash_operator '2020-12-20 20:17:44.157211+00:00'
```

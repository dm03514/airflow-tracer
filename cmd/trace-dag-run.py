import argparse
import collections
import datetime
import queue
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

from airflow.models import serialized_dag

trace.set_tracer_provider(TracerProvider())

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="airflow",
    agent_host_name="localhost",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(
        jaeger_exporter,
    )
)

tracer = trace.get_tracer(__name__)


def dt_to_ns_epoch(dt):
    return int(dt.timestamp() * 1000000000)


def main(cli=None):

    # it may be that the dag is updated in the db to a version that no longer reflects historic runs...
    dag = serialized_dag.SerializedDagModel.get(dag_id=cli.dag_id)
    dagrun = dag.dag.get_dagrun(execution_date=cli.execution_date)
    tis = dagrun.get_task_instances()

    root_span = tracer.start_span(
        name=dag.dag.dag_id,
        start_time=dt_to_ns_epoch(dagrun.start_date)
    )
    root_span.end(end_time=dt_to_ns_epoch(dagrun.end_date))

    for ti in tis:
        ctx = trace.set_span_in_context(root_span)

        span = tracer.start_span(
            name=ti.task_id,
            context=ctx,
            start_time=dt_to_ns_epoch(ti.start_date),
        )
        # span.set_attribute('airflow.pool', ti.pool)
        # span.set_attribute('airflow.queue', ti.queue)
        span.set_attribute('airflow.state', ti.state)
        span.set_attribute('airflow.operation', ti.operator)
        # span.set_attribute('airflow.max_tries', ti.max_tries)
        if ti.job_id is not None:
            span.set_attribute('airflow.job_id', ti.job_id)
        # span.set_attribute('airflow.pool_slots', ti.pool_slots)
        # span.set_attribute('airflow.priority_weight', ti.priority_weight)
        if ti.state != 'success':
            span.set_attribute('error', True)
        span.end(end_time=dt_to_ns_epoch(ti.end_date))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trace an individual Dag run')
    parser.add_argument('dag_id', help='dag id')
    parser.add_argument(
        'execution_date',
        type=datetime.datetime.fromisoformat,
        help='execution date of the dag run'
    )
    main(parser.parse_args())


import argparse
import collections
import datetime
import queue

from airflow.models import serialized_dag


class Node:
    def __init__(self, task_id, task_type):
        self.task_id = task_id
        self.task_type = task_type


class Graph:
    def __init__(self, dag):
        self.dag = dag
        self.graph = collections.defaultdict(list)
        self.tasks = {}
        for task in dag['dag']['tasks']:
            self.tasks[task['task_id']] = task
            self.graph[task['task_id']].extend(task['_downstream_task_ids'])
        self.graph = dict(self.graph)

    def bfs(self):
        # get all nodes that don't have parents
        q = queue.Queue()
        print(self.graph)
        for n in self.graph:
            for n2, edges in self.graph.items():
                if n in edges:
                    break
            else:
                q.put(n)



def main(cli=None):
    # it may be that the dag is updated in the db to a version that no longer reflects historic runs...
    dag = serialized_dag.SerializedDagModel.get(dag_id=cli.dag_id)
    g = Graph(dag.data)
    g.bfs()

    dagrun = dag.dag.get_dagrun(execution_date=cli.execution_date)
    tis = dagrun.get_task_instances()

    import ipdb; ipdb.set_trace();

    # construct the dag as a graph

    # setup the tracer

    # iterate the dag invocation creating a trace per span
    print(cli)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trace an individual Dag run')
    parser.add_argument('dag_id', help='dag id')
    parser.add_argument(
        'execution_date',
        type=datetime.datetime.fromisoformat,
        help='execution date of the dag run'
    )
    main(parser.parse_args())


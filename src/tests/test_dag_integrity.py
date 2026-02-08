import unittest

from airflow.models import DagBag


class TestDagIntegrity(unittest.TestCase):
    LOAD_THRESHOLD = 2

    def setUp(self):
        self.dagbag = DagBag(dag_folder="src/dags", include_examples=False)

    def test_import_errors(self):
        """
        Test if there are any import errors in the DAGs.
        """
        self.assertEqual(
            len(self.dagbag.import_errors),
            0,
            f"DAG import errors: {self.dagbag.import_errors}",
        )

    def test_dags_count(self):
        """
        Test if at least one DAG is loaded.
        """
        self.assertGreater(len(self.dagbag.dags), 0, "No DAGs found in the dag_folder.")

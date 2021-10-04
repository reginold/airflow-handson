from datetime import timedelta


class TestDagValidation:

    LOAD_SCECOND_THRESHOLD = timedelta(seconds=5)
    EXPECTED_NUMBER_OF_DAGS = 30

    def test_import_dags(self, dagbag):
        """
        Verify the Airflow is able to import all DAGs in the repo
        - check the typos
        - check the cycles
        """
        assert len(dagbag.import_errors) == 0, "DAG failures detected! Got: {}".format(
            dagbag.import_errors
        )

    def test_time_import_dags(self, dagbag):
        """
        Verify the DAGs load fast enough
        - check for loading time
        """
        stats = dagbag.dagbag_stats
        slow_dags = list(
            filter(lambda f: f.duration > self.LOAD_SCECOND_THRESHOLD, stats)
        )
        res = ", ".join(map(lambda f: f.file[1:], slow_dags))

        assert (
            len(slow_dags) == 0
        ), "The following DAGs take more than {0}s to load: {1}".format(
            self.LOAD_SCECOND_THRESHOLD, res
        )

    def test_number_of_dags(self, dagbag):
        """
        Verify the total number of DAGs is correct
        - check number of dags
        """
        stats = dagbag.dagbag_stats
        dag_num = sum([i.dag_num for i in stats])
        assert (
            dag_num == self.EXPECTED_NUMBER_OF_DAGS
        ), "Wrong number of dags, {0} expected got {1} (Can be due to cycles!)".format(
            self.EXPECTED_NUMBER_OF_DAGS, dag_num
        )

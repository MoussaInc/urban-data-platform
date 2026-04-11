from dag.urban_dag import dag

def test_dag_loaded():
    assert dag is not None

def test_task_count():
    assert len(dag.tasks) == 8  # 7 BashOperators + 1 dbt_tests

def test_dependencies():
    stg = dag.get_task("stg_osm_features")
    building = dag.get_task("building")
    assert building in stg.downstream_list

def test_urban_density_has_3_upstreams():
    score = dag.get_task("urban_density_score")
    upstream_ids = {t.task_id for t in score.upstream_list}
    assert upstream_ids == {"building_by_cities", "amenities_by_city", "roads"}
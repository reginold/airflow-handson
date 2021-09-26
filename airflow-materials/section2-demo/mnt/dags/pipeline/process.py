def second_task(**context):
    print("This is ----------- task 2")
    return "hoge======"


def third_task(**context):
    output = context["task_instance"].xcom_pull(task_ids="python_task_2")
    print("This is ----------- task 3")
    return "This is the result : " + output

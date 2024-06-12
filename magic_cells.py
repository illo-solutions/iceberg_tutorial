import os

import boto3
import awswrangler as wr
from IPython.core.magic import register_cell_magic

SAVED_VARS = {}

def get_var(var_name):
    return SAVED_VARS.get(var_name)

def _parse_cell_args(arg_line: str):
    args = arg_line.split()
    match args:
        case [database, destination_var]:
            return {"database": database, "destination_var": destination_var}
        case [database]:
            return {"database": database}
        case _:
            raise Exception()


@register_cell_magic
def athena(arg_line: str, sql_query: str):
    if not arg_line:
        raise ValueError("The command must be called like this: athena <database> [<destination_var>]")

    args = _parse_cell_args(arg_line)
    if "database" not in args:
        raise Exception()

    print("Executing SQL on Database:", args["database"])
    if "{DATA_BUCKET}" in sql_query:
        sql_query = sql_query.format(DATA_BUCKET=os.environ["DATA_BUCKET"])
    print('SQL Query to execute', sql_query, sep='\n')
    df = wr.athena.read_sql_query(sql_query, database=args["database"])

    if "destination_var" in args:
        print("Saving result of the SQL in variable:", args["destination_var"])
        SAVED_VARS[args["destination_var"]] = df

    return df

@register_cell_magic
def athena_exec(arg_line: str, sql_query: str):
    if not arg_line:
        raise ValueError("The command must be called like this: athena_exec <database>")

    args = _parse_cell_args(arg_line)
    if "database" not in args:
        raise Exception()

    print("Executing SQL on Database:", args["database"])
    if "{DATA_BUCKET}" in sql_query:
        sql_query = sql_query.format(DATA_BUCKET=os.environ['DATA_BUCKET'])

    response = boto3.client('athena').start_query_execution(
        QueryString=sql_query,
        QueryExecutionContext={
            'Database': args["database"]
        },
        ResultConfiguration={
            'OutputLocation': f"s3://{os.environ['DATA_BUCKET']}/athena_results/",
        }
    )
    return response

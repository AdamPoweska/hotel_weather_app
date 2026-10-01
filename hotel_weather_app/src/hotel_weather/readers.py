
def data_read(spark, file_ext, schema, file_dir):
    """
    Returns hotel df/dataframe.
    """
    return (
        spark.read
        .option("header", True)
        .option("recursiveFileLookup", True)
        .option("pathGlobFilter", file_ext)
        .schema(schema)
        .csv(file_dir)
    )

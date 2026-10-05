def data_read(spark, file_ext, schema, file_dir, file_format="csv"):
    reader = (
        spark.read
        .format(file_format)
        .option("recursiveFileLookup", True)
        .option("pathGlobFilter", file_ext)
    )
    if file_format == "csv":
        reader = reader.option("header", True).schema(schema)
    return reader.load(file_dir)
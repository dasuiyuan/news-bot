from pymilvus import MilvusClient, DataType

client = MilvusClient(uri='http://localhost:19530')
print(client.list_collections())

collection_name = "index_sy"
dim = 128

schema = client.create_schema(
    auto_id=False,
    enable_dynamic_schema=True,
)
schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=dim)

index_params = client.prepare_index_params()
index_params.add_index(field_name="vector", index_type="HNSW", metric_type="COSINE", params={})
client.drop_collection(collection_name=collection_name)
client.create_collection(collection_name=collection_name, schema=schema, index_params=index_params)
print(client.describe_index(collection_name=collection_name, index_name="vector"))

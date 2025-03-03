from pymongo import MongoClient



cluster = MongoClient("mongodb+srv://user:12345@myfirstcluster.eifhy.mongodb.net/?retryWrites=true&w=majority&appName=myFirstCluster")
db_name = cluster["fraud_detection"]  # Database name you want to connect to

col=db_name["dataa"]
col.insert_one({"name":"krishna"})
# print(f"Successfully connected to database: {db_name}")


 



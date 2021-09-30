# # import boto3

# ACCESS_KEY = "AKIA5LZQ2CELLJW7FK3Q"
# SECRET_KEY = "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"
# # REGION_NAME = "ap-northeast-1"


# # def upload_file():
# #     """push the file to s3"""
# #     client = boto3.client(
# #         "s3",
# #         aws_access_key=ACCESS_KEY,
# #         aws_secret_access_key=SECRET_KEY,
# #         region_name=REGION_NAME,
# #     )

# #     with open("/usr/local/airflow/dags/test.csv", "rb") as f:
# #         client.upload_fileobj(f, "lu-airflow", "test.csv")

# #     print("Upload Completed")
# #     print("........")


# # upload_file()

# import logging
# import os

# import boto3
# from botocore.exceptions import ClientError


# def upload_file(file_name, bucket, object_name=None):
#     """Upload a file to an S3 bucket

#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = os.path.basename(file_name)

#     s3 = boto3.resource(
#         "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=ACCESS_KEY
#     )

#     # Upload the file
#     s3_client = boto3.client("s3")
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True


# upload_file(file_name="test.csv", bucket="lu-airflow")

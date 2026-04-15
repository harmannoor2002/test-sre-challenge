from fastapi import FastAPI, UploadFile, File, Form
import boto3
import uuid
import os

app = FastAPI()

# -------------------------
# AWS CONFIG (FIXED)
# -------------------------
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

BUCKET_NAME = "test-sre-bucket-2026"
TABLE_NAME = "test-sre-users"

table = dynamodb.Table(TABLE_NAME)

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def root():
    return {"status": "API running"}

# -------------------------
# POST USER + IMAGE
# -------------------------
@app.post("/user")
async def create_user(
    email: str = Form(...),
    file: UploadFile = File(...)
):

    file_key = f"{uuid.uuid4()}-{file.filename}"

    # Upload to S3
    s3.upload_fileobj(file.file, BUCKET_NAME, file_key)

    file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_key}"

    # Save to DynamoDB
    table.put_item(
        Item={
            "email": email,
            "image_url": file_url
        }
    )

    return {
        "message": "User created successfully",
        "email": email,
        "image_url": file_url
    }

# -------------------------
# GET USERS
# -------------------------
@app.get("/users")
def get_users():
    response = table.scan()
    return {
        "users": response.get("Items", [])
    }

import os
import logging
import azure.functions as func
from datetime import datetime
from github import Github


from .models import Label, Participant, Meeting, create_tables, database_location
from .auth import get_token_from_auth_header, verify_decode_jwt, check_permissions, PERMISSION

ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
REPO_FULL_NAME = "ElGarash/Jitsi-Meetings-Dashboard"
TARGET_BRANCH = "gh-pages"


def main(req: func.HttpRequest) -> func.HttpResponse:
    token, token_err = get_token_from_auth_header(req)
    if token_err:
        return func.HttpResponse(token_err.message, status_code=token_err.status_code)
    payload, payload_err = verify_decode_jwt(token)
    if payload_err:
        return func.HttpResponse(payload_err.message, status_code=payload_err.status_code)
    permissions_err = check_permissions(PERMISSION, payload)
    if permissions_err:
        return func.HttpResponse(permissions_err.message, status_code=permissions_err.status_code)

    g = Github(ACCESS_TOKEN)
    repo = g.get_repo(REPO_FULL_NAME)
    db_file_contents = repo.get_contents("database.db", ref=TARGET_BRANCH)
    with open(database_location, "wb") as db_file:
        db_file.write(db_file_contents.decoded_content)

    request_body = req.get_json()
    insert_into_db(request_body)

    with open(database_location, "rb") as db_file:
        updated_content = db_file.read()

    repo.update_file(
        path=db_file_contents.path,
        message=f'Azure at "{datetime.now().strftime("%B %d, %Y - %I:%M %p")}"',
        content=updated_content,
        sha=db_file_contents.sha,
        branch=TARGET_BRANCH,
    )

    return func.HttpResponse("Successful operation", status_code=200)


def insert_into_db(data):
    create_tables()  # Create the tables if not already created.
    meeting_date = datetime.now()
    Meeting(date=meeting_date).insert()
    participants = data.get("participants", [])
    labels = data.get("labels", [])
    for participant in participants:
        Participant(name=participant, meeting_date=meeting_date).insert()
    for label in labels:
        Label(name=label, meeting_date=meeting_date).insert()

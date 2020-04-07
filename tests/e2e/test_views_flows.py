# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""End-2-End module tests."""


def test_create_record(base_client):
    """Test record creation."""

    # Create draft
    draft = base_client.post("/experimental/records")
    assert draft.status_code == 201  # Draft created

    # Get draft id
    rec_uuid = draft.json.get("id", None)
    assert rec_uuid is not None

    # Update with draft content
    draft_content = draft.json.get("metadata")
    # TODO: Add some new metadata
    draft = base_client.put(
        "/experimental/records/{}/drafts".format(rec_uuid), data=draft_content
    )
    assert draft.status_code == 200

    # TODO: Add case where validation fails

    # TODO: Upload a file through Invenio
    draft_file = base_client.put(
        "/experimental/records/{}/drafts/files/test.jpg".format(rec_uuid)
    )
    draft_file.status_code = 200

    # Publish record
    action = base_client.post(
        "/experimental/records/{}/drafts/actions/publish".format(rec_uuid)
    )
    # Accept publishing. Might lunch async tasks.
    assert action.status_code == 202

    # Get published record
    record = base_client.get("/experimental/records/{}".format(rec_uuid))
    assert record.status_code == 200
    assert record.json.get("id") == rec_uuid


def test_edit_record(base_client):
    """Test editing an existing record (new revision)."""

    # Create draft
    draft = base_client.post(
        "/experimental/records/{}/drafts".format("a1b2c-3d4e5")
    )
    assert draft.status_code == 201  # Draft created

    # Get draft id
    rec_uuid = draft.json.get("id", None)
    assert rec_uuid == "a1b2c-3d4e5"

    # Update with draft content
    draft_content = draft.json.get("metadata")
    # TODO: Add some new metadata
    draft = base_client.put(
        "/experimental/records/{}/drafts".format(rec_uuid), data=draft_content
    )
    assert draft.status_code == 200

    # Publish record
    action = base_client.post(
        "/experimental/records/{}/drafts/actions/publish".format(rec_uuid)
    )
    # Accept publishing. Might lunch async tasks.
    assert action.status_code == 202

    # Get published record
    record = base_client.get("/experimental/records/{}".format(rec_uuid))
    assert record.status_code == 200
    assert record.json.get("id") == rec_uuid


def test_create_new_version(base_client):
    """Test creation of a new version of a record."""

    # Create a new version
    old_rec_uuid = "a1b2c-3d4e5"
    draft = base_client.post(
        "/experimental/records/{}/versions".format(old_rec_uuid)
    )
    assert draft.status_code == 201  # Draft created

    # Get draft id
    rec_uuid = draft.json.get("id", None)
    assert rec_uuid != old_rec_uuid

    # Update with draft content
    draft_content = draft.json.get("metadata")
    # TODO: Add some new metadata
    draft = base_client.put(
        "/experimental/records/{}/drafts".format(rec_uuid), data=draft_content
    )
    assert draft.status_code == 200

    # Publish record
    action = base_client.post(
        "/experimental/records/{}/drafts/actions/publish".format(rec_uuid)
    )
    # Accept publishing. Might lunch async tasks.
    assert action.status_code == 202

    # Get published record
    record = base_client.get("/experimental/records/{}".format(rec_uuid))
    assert record.status_code == 200
    assert record.json.get("id") == rec_uuid

    # Get the previous version
    prev_ver = base_client.get(
        "/experimental/records/{}/versions/{}".format(old_rec_uuid, 1)
    )
    assert prev_ver.status_code == 200
    assert prev_ver.json.get("id") == old_rec_uuid
    assert prev_ver.json["metadata"]["version"] == "1"

    # Get the new version
    curr_ver = base_client.get(
        "/experimental/records/{}/versions/{}".format(rec_uuid, 2)
    )
    assert curr_ver.status_code == 200
    assert curr_ver.json.get("id") == rec_uuid
    assert curr_ver.json["metadata"]["version"] == "2"


def test_search_records(base_client):
    """Test search published records."""

    draft = base_client.get("/experimental/records")
    assert draft.status_code == 200  # Draft created
    assert len(draft.json.get("hits").get("hits")) == 2

    # TODO: perform a search with terms


def test_search_records_drafts(base_client):
    """Test search all records editable by the user."""

    draft = base_client.get("/experimental/records/editable")
    assert draft.status_code == 200  # Draft created
    assert len(draft.json.get("hits").get("hits")) == 2

    # TODO: perform a search with terms


def test_delete_record(base_client):
    """Test deletion of a published record."""

    draft = base_client.delete(
        "/experimental/records/{}".format("a1b2c-3d4e5")
    )
    assert draft.status_code == 202

    # TODO: Implement with permissions (should be admin only)
    # TODO: Assert fails to delete a not published record (draft)
    # TODO: Assert fails to delet a non-existing recid


# TODO: Test case for delete non-published draft
# TODO: Test case for delete published records' draft
# TODO: Test case with external upload of files

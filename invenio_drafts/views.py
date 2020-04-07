# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module to manage record drafts (deposits)."""

from flask import Blueprint, render_template, make_response
from flask.views import MethodView
from flask_babelex import gettext as _
from functools import wraps
from invenio_rdm_records.cli import create_fake_record

from .demo import (
    create_fake_record,
    create_fake_record_list,
    create_fake_new_record,
)


def pass_record(f):
    """Decorator to retrieve persistent identifier and record.
    This decorator will resolve the ``pid_value`` parameter from the route
    pattern and resolve it to a PID and a record, which are then available in
    the decorated function as ``pid`` and ``record`` kwargs respectively.
    """

    @wraps(f)
    def inner(self, pid_value, *args, **kwargs):
        # try:
        record = create_fake_record(rec_uuid=pid_value)
        return f(self, record=record, *args, **kwargs)
        # except SQLAlchemyError:
        #     raise PIDResolveRESTError(pid)

    return inner


def create_blueprint(app):
    """Create blueprint for drafts"""

    blueprint = Blueprint(
        "invenio_drafts",
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    resource_list = [
        RecordsListResource,
        RecordResource,
        DraftResource,
        RecordsDraftsMixResource,
        # RecordActionResource,
        DraftActionResource,
        VersionsListResource,
        VersionResource,
        RecordFilesListResource,
        DraftFilesListResource,
        RecordFileResource,
        DraftFileResource,
    ]

    for resource in resource_list:
        blueprint.add_url_rule(
            rule=resource.rule,
            view_func=resource.as_view(resource.view_name),
            methods=resource.methods,
        )

    return blueprint


# Records
# =======


class RecordsListResource(MethodView):
    """RecordsList item resource."""

    rule = "/experimental/records"
    view_name = "records_list"
    methods = ["POST", "GET"]

    def post(self, **kwargs):
        """Create new draft for new record from nothing."""
        return make_response(create_fake_new_record(), 201)

    def get(self, **kwargs):
        """Search (published) records."""
        return make_response(create_fake_record_list(), 200)


class RecordResource(MethodView):
    """Record item resource."""

    rule = "/experimental/records/<pid_value>"
    view_name = "record"
    methods = ["GET", "DELETE"]

    @pass_record
    def get(self, record, **kwargs):
        """Get a record."""
        return make_response(record, 200)

    @pass_record
    def delete(self, record, **kwargs):
        """Delete a record."""
        return make_response("Accepted", 202)


class RecordsDraftsMixResource(MethodView):
    """RecordsDraftsMix item resource."""

    rule = "/experimental/records/editable"
    view_name = "records_drafts"
    methods = ["GET"]

    def get(self, **kwargs):
        """Search and display mix of records and drafts."""

        return make_response(create_fake_record_list(), 200)


# Drafts
# =======


class DraftResource(MethodView):
    """Draft item resource."""

    rule = "/experimental/records/<pid_value>/drafts"
    view_name = "draft"
    methods = ["POST", "GET", "PUT", "DELETE"]

    @pass_record
    def post(self, record, **kwargs):
        """Create new draft for existing record from existing record."""
        return make_response(record, 201)

    @pass_record
    def get(self, record, **kwargs):
        """Get the latest record version draft.

        Note that a new version represents a new child record. Therefore,
        this returns a draft of the latest created child.
        """
        return make_response(record, 200)

    @pass_record
    def put(self, record, **kwargs):
        """Edit a record draft."""
        # Returns full record.
        # Assumes it got it as input and validation did not fail.
        return make_response(record, 200)

    # @pass_record
    def delete(self, **kwargs):
        """Discard a draft.

        Deletes also the record if it has not been published.
        """
        return make_response("Accepted", 202)


# Versions
# ========


class VersionsListResource(MethodView):
    """VersionsList item resource."""

    rule = "/experimental/records/<pid_value>/versions"
    view_name = "record_versions"
    methods = ["POST", "GET"]

    @pass_record
    def post(self, record, **kwargs):
        """Create new draft (version) for new record from existing record."""
        new_record = create_fake_new_record()
        new_record["metadata"] = record["metadata"]
        return make_response(new_record, 201)

    @pass_record
    def get(self, record, **kwargs):
        """Search versions of the record."""
        return make_response(record, 200)


class VersionResource(MethodView):
    """Version item resource."""

    rule = "/experimental/records/<pid_value>/versions/<version>"
    view_name = "record_version"
    methods = ["GET"]

    @pass_record
    def get(self, record, version, **kwargs):
        """Get a specific version of the record."""
        record["metadata"]["version"] = version
        return make_response(record, 200)


# Actions
# =======


class ActionResource(MethodView):
    """Action item resource."""

    methods = ["POST"]

    # Note: use factory to allow multiple routes.
    @pass_record
    def post(self, record, action, **kwargs):
        """Execute the <action> over:
        - the <record>.
        - the <draft>.

        POST	/records/:id/actions/:action	execute action
        POST	/records/:id/draft/actions/publish	Publish draft to record
        POST	/records/:id/draft/actions/:action	Execute action
        """
        return make_response("Accepted", 202)


# class RecordActionResource(ActionResource):
#     """Record actions item resource."""

#     rule = "/experimental/records/<pid_value>/actions/<action>"
#     view_name = "records_actions"


class DraftActionResource(ActionResource):
    """Record actions item resource."""

    rule = "/experimental/records/<pid_value>/drafts/actions/<action>"
    view_name = "drafts_actions"


# Files
# =====


class FilesListResource(MethodView):
    """FileList item resource."""

    methods = ["POST", "GET"]

    @pass_record
    def get(self, record, **kwargs):
        """Get files of the record."""
        pass

    @pass_record
    def delete(self, record, **kwargs):
        """Delete all files from the record."""
        pass


class RecordFilesListResource(FilesListResource):
    """RecordFileList item resource."""

    rule = "/experimental/records/<pid_value>/files/"
    view_name = "record_files"


class DraftFilesListResource(FilesListResource):
    """DraftFilesList item resource."""

    rule = "/experimental/records/<pid_value>/draft/files/"
    view_name = "draft_files"


class FileResource(MethodView):
    """File item resource."""

    methods = ["POST", "GET"]

    @pass_record
    def get(self, record, file, **kwargs):
        """Get a specific file of the record."""
        pass

    @pass_record
    def put(self, record, file, **kwargs):
        """Upload a file to the record."""
        pass

    @pass_record
    def delete(self, record, file, **kwargs):
        """Delete a file from the record."""
        pass


class RecordFileResource(FileResource):
    """RecordFile item resource."""

    rule = "/experimental/records/<pid_value>/files/<file>"
    view_name = "record_file"


class DraftFileResource(FileResource):
    """RecordFile item resource."""

    rule = "/experimental/records/<pid_value>/draft/files/<file>"
    view_name = "draft_file"

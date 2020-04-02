# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module to manage record drafts (deposits)"""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from flask import Blueprint, render_template
from flask_babelex import gettext as _

blueprint = Blueprint(
    'invenio_drafts',
    __name__,
    template_folder='templates',
    static_folder='static',
)


class RecordsListResource(ObjectResource):
    """RecordsList item resource."""

    def post(self, **kwargs):
        """Create new draft for new record from nothing."""
        pass

    def get(self, **kwargs):
        """Search (published) records."""
        pass


class RecordResource(ObjectResource):
    """Record item resource."""

    @pass_record
    def get(self, pid, record, **kwargs):
    """Get a record."""
    pass

    @pass_record
    def delete(self, pid, record, **kwargs):
    """Delete a record."""
    pass


class DraftsListResource(ObjectResource):
    """DraftsList item resource."""

    @pass_record
    def post(self, pid, record, **kwargs):
        """Create new draft for existing record from existing record."""
        pass


class DraftResource(ObjectResource):
    """Draft item resource."""

    @pass_record
    def get(self, pid, record, **kwargs):
        """Get the latest record version draft.

        Note that a new version represents a new child record. Therefore,
        this returns a draft of the latest created child.
        """
        pass

    @pass_record
    def put(self, pid, record, **kwargs):
        """Edit a record draft."""
        pass

    @pass_record
    def delete(self, pid, record, **kwargs):
        """Discard a draft.

        Deletes also the record if it has not been published.
        """
        pass


class RecordsDraftsMixResource(ObjectResource):
    """RecordsDraftsMix item resource."""

    def get(self, **kwargs):
        """Search and display mix of records and drafts."""
        pass


class ActionResource(ObjectResource):
    """Action item resource."""

    @pass_record
    @pass_action
    def post(self, pid, record, action, **kwargs):
        """Execute the <action> over:
        - the <record>.
        - the <draft>.

        POST	/records/:id/actions/:action	execute action
        POST	/records/:id/draft/actions/publish	Publish draft to record
        POST	/records/:id/draft/actions/:action	Execute action
        """
        pass


class VersionsListResource(ObjectResource):
    """VersionsList item resource."""

    @pass_record
    def post(self, pid, record, **kwargs):
        """Create new draft (version) for new record from existing record."""
        pass

    @pass_record
    def get(self, pid, record, **kwargs):
        """Search versions of the record."""
        pass


class VersionResource(ObjectResource):
    """Version item resource."""

    @pass_record
    @pass_version
    def get(self, pid, record, version, **kwargs):
        """Get a specific version of the record."""
        pass


class FilesListResource(ObjectResource):
    """FileList item resource."""

    @pass_record
    def get(self, pid, record, **kwargs):
        """Get files of the record."""
        pass

    @pass_record
    def delete(self, pid, record, **kwargs):
        """Delete all files from the record."""
        pass


class FileResource(ObjectResource):
    """File item resource."""

    @pass_record
    @pass_file
    def get(self, pid, record, file, **kwargs):
        """Get a specific file of the record."""
        pass

    @pass_record
    @pass_file
    def put(self, pid, record, file, **kwargs):
        """Upload a file to the record."""
        pass

    @pass_record
    @pass_file
    def delete(self, pid, record, file, **kwargs):
        """Delete a file from the record."""
        pass
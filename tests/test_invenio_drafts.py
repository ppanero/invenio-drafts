# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from flask import Flask

from invenio_drafts import InvenioDrafts


def test_version():
    """Test version import."""
    from invenio_drafts import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioDrafts(app)
    assert 'invenio-drafts' in app.extensions

    app = Flask('testapp')
    ext = InvenioDrafts()
    assert 'invenio-drafts' not in app.extensions
    ext.init_app(app)
    assert 'invenio-drafts' in app.extensions


def test_view(base_client):
    """Test view."""
    res = base_client.get("/")
    assert res.status_code == 200
    assert 'Welcome to Invenio-Drafts' in str(res.data)

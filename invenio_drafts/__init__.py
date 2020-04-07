# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module to manage record drafts (deposits)."""

from .ext import InvenioDrafts
from .version import __version__

__all__ = ("__version__", "InvenioDrafts")

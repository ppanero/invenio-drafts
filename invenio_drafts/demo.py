# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""TODO: Remove when data is not mocked."""


import datetime
import random
import uuid

from edtf.parser.grammar import level0Expression
from faker import Faker
from invenio_rdm_records.vocabularies import Vocabulary


def fake_resource_type():
    """Generates a fake resource_type."""
    vocabulary = Vocabulary.get_vocabulary("resource_types")
    _type, subtype = random.choice(list(vocabulary.data.keys()))
    return {"type": _type, "subtype": subtype}


def fake_edtf_level_0():
    """Generates a fake publication_date string."""

    def fake_date(end_date=None):
        fake = Faker()
        date_pattern = ["%Y", "%m", "%d"]
        # make it less and less likely to get less and less parts of the date

        if random.choice([True, False]):
            date_pattern.pop()
            if random.choice([True, False]):
                date_pattern.pop()

        return fake.date("-".join(date_pattern), end_datetime=end_date)

    f_date = fake_date()

    # if interval
    if random.choice([True, False]):
        # get f_date as date object
        parser = level0Expression("level0")
        parsed_date = parser.parseString(f_date)[0]
        date_tuple = parsed_date.lower_strict()[:3]
        f_date_object = datetime.date(*date_tuple)

        interval_start = fake_date(end_date=f_date_object)

        return "/".join([interval_start, f_date])

    return f_date


def create_fake_new_record():
    """Generates a fake new record."""
    id = uuid.uuid4()
    return {
        "created": "2020-04-06T15:24:12.396419+00:00",
        "id": id,
        "links": {
            "files": "https://localhost:5000/api/experimental/records/{}/files".format(
                id
            ),
            "self": "https://localhost:5000/api/experimental/records/{}".format(
                id
            ),
        },
        "revision": 0,
        "updated": "2020-04-06T15:24:12.396424+00:00",
        "metadata": {},
    }


def create_fake_record(rec_uuid=None):
    """Create full record."""
    fake = Faker()
    data_to_use = {
        "_access": {"metadata_restricted": False, "files_restricted": False},
        "_created_by": 2,
        "_default_preview": "previewer one",
        "_internal_notes": [
            {
                "user": "inveniouser",
                "note": "RDM record",
                "timestamp": fake.iso8601(tzinfo=None, end_datetime=None),
            }
        ],
        "_owners": [1],
        "access_right": "open",
        "embargo_date": fake.iso8601(tzinfo=None, end_datetime=None),
        "contact": "info@inveniosoftware.org",
        "community": {
            "primary": "Maincom",
            "secondary": ["Subcom One", "Subcom Two"],
        },
        "resource_type": fake_resource_type(),
        "identifiers": {"DOI": "10.9999/rdm.9999999", "arXiv": "9999.99999",},
        "creators": [
            {
                "name": fake.name(),
                "type": "Personal",
                "identifiers": {"Orcid": "9999-9999-9999-9999",},
                "affiliations": [
                    {
                        "name": fake.company(),
                        "identifier": "entity-one",
                        "scheme": "entity-id-scheme",
                    }
                ],
            }
        ],
        "titles": [
            {
                "title": fake.company() + "'s gallery",
                "type": "Other",
                "lang": "eng",
            }
        ],
        "publication_date": fake_edtf_level_0(),
        "subjects": [
            {
                "subject": "Romans",
                "identifier": "subj-1",
                "scheme": "no-scheme",
            }
        ],
        "contributors": [
            {
                "name": fake.name(),
                "type": "Personal",
                "identifiers": {"Orcid": "9999-9999-9999-9998",},
                "affiliations": [
                    {
                        "name": fake.company(),
                        "identifier": "entity-one",
                        "scheme": "entity-id-scheme",
                    }
                ],
                "role": "RightsHolder",
            }
        ],
        "dates": [
            {
                # No end date to avoid computations based on start
                "start": fake.iso8601(tzinfo=None, end_datetime=None),
                "description": "Random test date",
                "type": "Other",
            }
        ],
        "language": "eng",
        "related_identifiers": [
            {
                "identifier": "10.9999/rdm.9999988",
                "scheme": "DOI",
                "relation_type": "Requires",
                "resource_type": fake_resource_type(),
            }
        ],
        "version": "v0.0.1",
        "licenses": [
            {
                "license": "Berkeley Software Distribution 3",
                "uri": "https://opensource.org/licenses/BSD-3-Clause",
                "identifier": "BSD-3",
                "scheme": "BSD-3",
            }
        ],
        "descriptions": [
            {
                "description": fake.text(max_nb_chars=3000),
                "type": "Abstract",
                "lang": "eng",
            }
        ],
        "locations": [
            {
                "point": {
                    "lat": str(fake.latitude()),
                    "lon": str(fake.longitude()),
                },
                "place": fake.location_on_land()[2],
                "description": "Random place on land for random coordinates...",
            }
        ],
        "references": [
            {
                "reference_string": "Reference to something et al.",
                "identifier": "9999.99988",
                "scheme": "GRID",
            }
        ],
    }

    # Create and index record
    id = uuid.uuid4() if not rec_uuid else rec_uuid

    return {
        "created": "2020-04-06T15:24:12.396419+00:00",
        "id": id,
        "links": {
            "files": "https://localhost:5000/api/experimental/records/{}/files".format(
                id
            ),
            "self": "https://localhost:5000/api/experimental/records/{}".format(
                id
            ),
        },
        "revision": 0,
        "updated": "2020-04-06T15:24:12.396424+00:00",
        "metadata": data_to_use,
    }


def create_fake_record_list():
    """Generates a fake records list."""
    return {
        "aggregations": {
            "access_right": {
                "buckets": [{"doc_count": 10, "key": "open"}],
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
            }
        },
        "hits": {"hits": [create_fake_record(), create_fake_record()]},
        "links": {
            "self": "https://localhost:5000/api/experimental/records/?sort=mostrecent&size=10&page=1"
        },
    }


def create_fake_file():
    """Create a fake file meta."""

    return {
        "version_id": "370cba0b-4b7d-4e56-916f-f8f9606e8f09",
        "key": "snow_doge.jpg",
        "delete_marker": False,
        "updated": "2020-04-07T13:37:42.898265",
        "created": "2020-04-07T13:37:42.893365",
        "is_head": True,
        "checksum": "md5:3a695fc209fb948cd70fd710f92d1ae0",
        "mimetype": "image/jpeg",
        "links": {
            "self": "https://localhost:5000/api/records/tbwnh-dyw64/files/snow_doge.jpg",
            "version": "https://localhost:5000/api/records/tbwnh-dyw64/files/snow_doge.jpg?versionId=370cba0b-4b7d-4e56-916f-f8f9606e8f09",
            "uploads": "https://localhost:5000/api/records/tbwnh-dyw64/files/snow_doge.jpg?uploads",
        },
        "size": 133012,
        "tags": {},
    }


def create_fake_files_list():
    """Create a fake list of files."""

    return {
        "contents": [create_fake_file(), create_fake_file()],
        "id": "55cb796b-5ffa-4c1f-943f-0b1731013e8e",
        "max_file_size": None,
        "updated": "2020-04-07T13:37:42.904294",
        "quota_size": None,
        "created": "2020-04-06T15:24:12.387537",
        "locked": False,
        "links": {
            "self": "https://localhost:5000/api/records/tbwnh-dyw64/files",
            "versions": "https://localhost:5000/api/records/tbwnh-dyw64/files?versions",
            "uploads": "https://localhost:5000/api/records/tbwnh-dyw64/files?uploads",
        },
        "size": 266024,
    }

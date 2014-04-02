import os

from os.path import abspath, dirname, join

SCRAPER_PATHS=[os.path.join(os.getcwd(), 'openstates')]
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'fiftystates'

LEGISLATOR_FILTERS = {
    "billy.importers.filters.single_space_filter": [
        "full_name",
        "first_name",
        "last_name",
        "middle_name",
    ],
    "billy.importers.filters.phone_filter": [
        "office_phone",
        "phone",
        "offices.phone",
        "offices.fax",
    ],
    "billy.importers.filters.email_filter": [
        "offices.email",
    ],
}

BILL_FILTERS = {
    "billy.importers.filters.single_space_filter": [
        "actions.action",
        "title",
    ]
}

EVENT_FILTERS = {
    "billy.importers.filters.single_space_filter": [
        "description",
        "participants.participant",
        "related_bills.bill_id",
        "related_bills.description",
    ]
}


try:
    from billy_local import *
except ImportError:
    pass

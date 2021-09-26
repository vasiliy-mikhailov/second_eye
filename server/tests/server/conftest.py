import pytest
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import demo_extract
from server.wsgi import *
from django.conf import settings

@pytest.fixture(scope="module")
def graphene_client():
  extractor = demo_extract.Extractor()
  settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=extractor)
  client = Client(schema.schema)
  return client
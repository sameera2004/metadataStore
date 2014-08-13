__author__ = 'arkilic'
import random
import datetime
import unittest

from pymongo.errors import DuplicateKeyError

from metadataStore.database.databaseTables import Header
from metadataStore.sessionManager.databaseInit import db


class TestHeaderObject(unittest.TestCase):
    """
    Tests Included:
        scan_id uniqueness
        Header save data verification
        scan_id querying given uniqueness of
    """
    def setUp(self):
        self.s_id = random.randint(0,1000)
        self.s_id2 = self.s_id + 1
        self._id = Header(start_time=datetime.datetime.utcnow(), scan_id=self.s_id, beamline_id='csx',
                          owner='arkilic', custom={'attribute': 'value'}).save(wtimeout=100, write_concern={'w': 1})
        self._id2 = Header(start_time=datetime.datetime.utcnow(),
                           scan_id=self.s_id2, beamline_id='csx').save(wtimeout=100, write_concern={'w': 1})

    def test_scan_id_uniqueness(self):
        hdr = Header(start_time=datetime.datetime.utcnow(), scan_id=self.s_id, beamline_id='csx',
                     owner='arkilic', custom={'attribute': 'value'})
        self.assertRaises(DuplicateKeyError, hdr.save, wtimeout=100, write_concern={'w': 1})

    def test_scan_id_given_id(self):
        query_cursor = db['header'].find({'_id': self._id2})
        self.assertEquals('csx', query_cursor[0]['beamline_id'], 'Incorrect beamline_id')
        self.assertEquals(self.s_id2, query_cursor[0]['scan_id'], 'Incorrect scan_id')

    def test_time_format(self):
        self.assertRaises(TypeError, Header, start_time='08/13/2014-08:23:19', scan_id=self.s_id, beamline_id='csx',
                          owner='arkilic', custom={'attribute': 'value'})
        self.assertRaises(TypeError, Header, scan_id=self.s_id, beamline_id='csx',
                          owner='arkilic', custom={'attribute': 'value'}, end_time='08/13/2014-08:23:19')

    def test_status(self):
        self.assertRaises(TypeError, Header, start_time='08/13/2014-08:23:19', scan_id=self.s_id, beamline_id='csx',
                          owner='arkilic', custom={'attribute': 'value'}, status=134)

    def test_custom(self):
        self.assertRaises(TypeError, Header, start_time='08/13/2014-08:23:19', scan_id=self.s_id, beamline_id='csx',
                          owner='arkilic', custom={'attribute': 'value'}, status=134)

    def tearDown(self):
        db['header'].remove({'_id': self._id})
        db['header'].remove({'_id': self._id2})
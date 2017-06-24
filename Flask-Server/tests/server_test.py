import os
import server
import unittest
import tempfile

class ServerTest(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['SQL_FILE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        with server.app.app_context():
            server.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

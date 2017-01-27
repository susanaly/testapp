# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 15:15:17 2017

@author: susanalaiyuen
"""

from flask import Flask, Request, request
from StringIO import StringIO
import unittest

RESULT = False

class TestFileFail(unittest.TestCase):
    def test_1(self):
        class FileObj(StringIO):
            def close(self):
                print 'in file close'
                global RESULT
                RESULT = True
        
        class MyRequest(Request):
            def _get_file_stream(*args, **kwargs):
                return FileObj()
        
        app = Flask(__name__)
        
        app.debug = True
        app.request_class = MyRequest
        
        # Test uploaded file
        @app.route("/uploader", methods=['POST'])
        def upload_file():
            f = request.files['file']
            print 'in upload handler'
            self.assertIsInstance(
                f.stream,
                FileObj,
                )
            f.close()
            return 'ok'
        
        client = app.test_client()
        resp = client.post(
            '/uploader',
            data = {'file': (StringIO('my file contents'), 'test.jpg'),})
        self.assertEqual('ok', resp.data,)
        global RESULT
        self.assertTrue(RESULT)


if __name__ == '__main__':
    unittest.main()
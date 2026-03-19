import unittest
import json
import os
import shutil
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterDocument(unittest.TestCase):
    def test_valid_pdf_document(self):
        system = EnterpriseManager()


        result = system.register_document("valid_pdf.json")


        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
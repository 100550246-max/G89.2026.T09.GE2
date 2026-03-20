"""Tests for the register_document method"""
import unittest
import json
import os
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterDocument(unittest.TestCase):
    """Class containing tests for register document"""

    def test_all_cases_from_master_json(self):
        """Tests all cases from the master JSON file"""

        with open("src/unittest/data/data_method_2.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        test_cases = data.get("test_cases", [])
        system = EnterpriseManager()

        for tc in test_cases:
            with self.subTest(msg=f"Running {tc['id_test']} - {tc['type']}"):

                temp_file = tc["file_path"]

                with open(temp_file, "w", encoding="utf-8") as temp_f:
                    temp_f.write(tc["content"])

                try:
                    if tc["expected_result"] == "EnterpriseManagementException":
                        with self.assertRaises(EnterpriseManagementException):
                            system.register_document(temp_file)
                    else:
                        result = system.register_document(temp_file)
                        self.assertIsNotNone(result)
                        self.assertIsInstance(result, str)
                        self.assertEqual(len(result), 64)
                finally:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

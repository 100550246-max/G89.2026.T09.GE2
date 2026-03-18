import unittest
import json
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterProject(unittest.TestCase):
    """Class for testing register_project using JSON data"""

    def test_register_project_from_json(self):
        """Execute all test cases from the JSON file"""
        #clean
        import os
        if os.path.exists("corporate_operations.json"):
            os.remove("corporate_operations.json")

        # Load the JSON file
        with open("src/unittest/data/data_method_1.json", "r") as f:
            data_list = json.load(f)

        my_manager = EnterpriseManager()

        for case in data_list:
            # For each case in the JSON, we extract the data
            with self.subTest(msg=f"Executing {case['id_test_case']}"):

                if case["expected_result"] == "VALID":
                    # If it's VALID, it should return a 32-char string without crashing
                    result = my_manager.register_project(
                        case["company_cif"],
                        case["project_acronym"],
                        case["operation_name"],
                        case["department"],
                        case["date"],
                        case["budget"]
                    )
                    self.assertEqual(len(result), 32)
                else:
                    # If it's INVALID, it MUST raise EnterpriseManagementException
                    with self.assertRaises(EnterpriseManagementException):
                        my_manager.register_project(
                            case["company_cif"],
                            case["project_acronym"],
                            case["operation_name"],
                            case["department"],
                            case["date"],
                            case["budget"]
                        )
if __name__ == '__main__':
    unittest.main()

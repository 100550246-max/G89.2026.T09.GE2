import unittest
import json
import os
import shutil
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestCheckProjectBudget(unittest.TestCase):

    def test_check_project_budget_from_json(self):
        """
        Executes all test cases for Method 3 from the JSON file.
        """
        # --- POINT TO THE FILE YOU HAVE IN PYCHARM ---
        test_file_path = "src/unittest/data/data_method_3.json"

        # Open and load the test cases
        with open(test_file_path, "r", encoding="utf-8") as file:
            test_cases = json.load(file)

        # Instantiate our manager
        my_manager = EnterpriseManager()

        # Paths for flows.json (located in the data folder based on your PyCharm)
        flows_file_original = "src/unittest/data/flows.json"
        flows_file_manager = "flows.json"  # Where the manager looks for it by default

        # Copy flows.json to the root folder so the manager can find it
        if os.path.exists(flows_file_original):
            shutil.copy(flows_file_original, flows_file_manager)

        # Loop through each test case
        for case in test_cases:
            tc_id = case["ID TEST"]
            project_id = case["project_id"]
            expected_result = case["Expected Result"]

            print(f"Executing {tc_id} for Method 3...")

            # --- TC5 TRAP ---
            # If it is TC5, delete flows.json from the root to trigger the exception
            if tc_id == "TC5" and os.path.exists(flows_file_manager):
                os.remove(flows_file_manager)

            # --- EXECUTE AND ASSERT ---
            try:
                if expected_result == "True":
                    # For the success case (TC7)
                    result = my_manager.check_project_budget(project_id)
                    self.assertTrue(result)
                else:
                    # For all failure cases (TC1 to TC6)
                    with self.assertRaises(EnterpriseManagementException) as context:
                        my_manager.check_project_budget(project_id)

                    # Check if the error message is exactly the expected one
                    self.assertEqual(context.exception.message, expected_result)

            finally:
                # --- RESTORE AFTER TC5 TRAP ---
                # Copy the file back so TC6 and TC7 do not fail
                if tc_id == "TC5" and os.path.exists(flows_file_original):
                    shutil.copy(flows_file_original, flows_file_manager)

        # Final camp cleanup (delete flows.json from root and the output file)
        if os.path.exists(flows_file_manager):
            os.remove(flows_file_manager)
        if os.path.exists("project_budgets.json"):
            os.remove("project_budgets.json")
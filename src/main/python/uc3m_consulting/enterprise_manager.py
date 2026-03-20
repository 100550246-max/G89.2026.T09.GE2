import os
import json
from datetime import datetime, timezone
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException



class EnterpriseManager:
    """Class for providing the methods for managing the projects"""

    def __init__(self):
        pass

# --- METHOD 1 ---

    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         operation_name: str,
                         department: str,
                         date: str,
                         budget: float) -> str:
        # --- CIF CHEKS ---

        # Check if the CIF is a string
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("CIF is not a valid string")

        # Check if the CIF length is exactly 9 characters
        if len(company_cif) != 9:
            if len(company_cif) < 9:
                raise EnterpriseManagementException("CIF length < 9")
            else:
                raise EnterpriseManagementException("CIF length > 9")

        # Validate the CIF format and checksum
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("Invalid CIF code")

        # --- PROJECT_ACRONYM CHECKS ---

        # Check if project_acronym is a string
        if not isinstance(project_acronym, str):
            raise EnterpriseManagementException("Project acronym is not a string")

        # Check if project_acronym has the required length
        if len(project_acronym) < 5:
            raise EnterpriseManagementException("Project acronym length < 5")

        if len(project_acronym) > 10:
            raise EnterpriseManagementException("Project acronym length > 10")

        # Check if it only contains alphanumeric characters (no special symbols)
        if not project_acronym.isalnum():
            raise EnterpriseManagementException("Invalid Project_acronym")

        # --- OPERATION_NAME CHECKS ---

        # Check if operation_name is a string
        if not isinstance(operation_name, str):
            raise EnterpriseManagementException("Operation_name is not a string")

        # Check if length is less than 10
        if len(operation_name) < 10:
            raise EnterpriseManagementException("Operation_name lenght < 10")

        # Check if length is greater than 30
        if len(operation_name) > 30:
            raise EnterpriseManagementException("Operation_name length > 30")

        # --- DEPARTMENT CHECKS ---

        # Check if department is a string
        if not isinstance(department, str):
            raise EnterpriseManagementException("Department is not a string")

        # Check if department is within the allowed options
        valid_departments = ["HR", "FINACE", "LEGAL", "LOGISTICS"]
        if department not in valid_departments:
            raise EnterpriseManagementException("Invalid department")

        # --- DATE CHECKS ---

        # Check if date is a string
        if not isinstance(date, str):
            raise EnterpriseManagementException("Date is not a string")

        # Check basic format DD/MM/YYYY
        if len(date) != 10:
            raise EnterpriseManagementException("Date is not in format DD/MM/YYYY")

        if date[2] != "/" or date[5] != "/":
            raise EnterpriseManagementException("Date is not in format DD/MM/YYYY")

        day_str, month_str, year_str = date.split("/")
        if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
            raise EnterpriseManagementException("Date is not in format DD/MM/YYYY")

        day = int(day_str)
        month = int(month_str)
        year = int(year_str)

        # Day limits (TC19 and TC20)
        if day < 1:
            raise EnterpriseManagementException("Date.day < 1")
        if day > 31:
            raise EnterpriseManagementException("Date.day > 31")

        # Month limits (TC21 and TC22)
        if month < 1:
            raise EnterpriseManagementException("Date.month < 1")
        if month > 12:
            raise EnterpriseManagementException("Date.month > 12")

        # Year limits (TC23 and TC24)
        if year < 2025:
            raise EnterpriseManagementException("Date.year < 2025")
        if year > 2027:
            raise EnterpriseManagementException("Date.year > 2027")

        # --- TC25: Date must be equal to or after today ---
        from datetime import datetime

        try:
            project_date = datetime(year, month, day).date()
            today_date = datetime.today().date()

            if project_date < today_date:
                raise EnterpriseManagementException("Invalid Date")
        except ValueError:
            # If the date is mathematically impossible,
            # catch it here to launch the exact error the Excel expects.
            raise EnterpriseManagementException("Invalid Date")

        # --- BUDGET CHECKS ---

        # Check if budget is a numeric value (TC26)
        if not isinstance(budget, float):
            raise EnterpriseManagementException("Budget is not a float")

        # Check budget limits (TC27 and TC28)
        if budget < 50000.00:
            raise EnterpriseManagementException("Budget < 50000.00")

        if budget > 1000000.00:
            raise EnterpriseManagementException("Budget > 1000000.00")

        # Check decimal limits (TC29 and TC30)
        str_budget = str(budget)
        if "." in str_budget:
            decimals = len(str_budget.split(".")[1])
            if decimals > 2:
                raise EnterpriseManagementException("Budget have more than 2 decimals")
            if decimals < 2:
                raise EnterpriseManagementException("Budget have less than 2 decimals")
        else:
            # If there is no dot (e.g., an integer), it has 0 decimals
            raise EnterpriseManagementException("Budget have less than 2 decimals")

        # --- P2: GENERATE PROJECT ID (MD5) ---
        import hashlib
        import json
        import os

        # Concatenate the input data to create a unique base for the hash
        # (If your teacher specified a specific order or format for this string, adjust it here)
        data_to_hash = f"{company_cif}{project_acronym}{operation_name}{department}{date}{budget}"

        # Generate the 32-character hexadecimal MD5 hash
        project_id = hashlib.md5(data_to_hash.encode('utf-8')).hexdigest()

        # --- P3: STORE DATA IN JSON FILE & CHECK DUPLICATES (CM-FR-01-O3) ---
        file_path = "corporate_operations.json"

        # Read the file if it exists
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data_list = json.load(file)
                except json.JSONDecodeError:
                    # If the file is empty or corrupted, start a fresh list
                    data_list = []
        else:
            data_list = []

        # CM-FR-01-O3: Check if a project with the same name for the same CIF already exists
        for record in data_list:
            # We check if both the CIF and the acronym (name) match an existing record
            if record.get("company_cif") == company_cif and record.get("project_acronym") == project_acronym:
                # ⚠️ ¡ATENCIÓN VIGÍA! Revisa si tu profesor pide un error exacto en las instrucciones.
                raise EnterpriseManagementException("Project already exists")

        # Create a dictionary with the project record
        project_record = {
            "Project_ID": project_id,
            "company_cif": company_cif,
            "project_acronym": project_acronym,
            "operation_name": operation_name,
            "department": department,
            "date": date,
            "budget": budget
        }

        # Append the new project and write back to the file
        data_list.append(project_record)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data_list, file, indent=4)

        # Return the generated MD5 hash as required by the method signature
        return project_id

    # --- METHOD 2 ---
    def register_document(self, input_file):
        import os
        import json
        import re
        import hashlib
        from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

        if type(input_file) is not str:
            raise EnterpriseManagementException("Invalid file path type")

        if not os.path.exists(input_file):
            raise EnterpriseManagementException("File not found")

        try:
            with open(input_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            raise EnterpriseManagementException("JSON Decode Error - Wrong format")

        if "PROJECT_ID" not in data:
            raise EnterpriseManagementException("Invalid PROJECT_ID key")
        if "FILENAME" not in data:
            raise EnterpriseManagementException("Invalid FILENAME key")

        project_id = data["PROJECT_ID"]
        filename = data["FILENAME"]

        if type(project_id) is not str or not re.fullmatch(r"^[0-9a-fA-F]{32}$", project_id):
            raise EnterpriseManagementException("Invalid PROJECT_ID format")

        data_to_hash = project_id + filename
        return hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()

    # --- METHOD 3 ---

    def check_project_budget(self, project_id: str):
        """
        Calculates the total budget for a given project_id by reading flows.json.
        """
        import os
        import json
        from datetime import datetime, timezone

        # --- NODES 1 & 2: Check if project_id is a string ---
        if type(project_id) != str:
            raise EnterpriseManagementException("Project ID is not a string")

        # --- NODES 3 & 4: Check if length is exactly 32 ---
        if len(project_id) != 32:
            raise EnterpriseManagementException("Project ID must have exactly 32 Characters")

        # --- NODES 5, 6 & 7: Check letters and numbers manually ---
        # Iterate through each character in the project_id
        for char in project_id:
            if char.isalpha():
                # Node 5: If it is a letter, it must be between a-f (or A-F)
                if char.lower() not in ['a', 'b', 'c', 'd', 'e', 'f']:
                    raise EnterpriseManagementException("Invalid Project Id")
            elif char.isdigit():
                # Node 7: If it is a number, it must be between 0-9
                # (char.isdigit() already guarantees it is 0-9, so we just pass)
                pass
            else:
                # If it's neither a letter nor a number (e.g., '-', '!', ' '), it fails
                raise EnterpriseManagementException("Invalid Project Id")

        # --- NODES 8 & 9: Existing json file? ---
        file_path = "flows.json"
        if not os.path.exists(file_path):
            raise EnterpriseManagementException("json file not founded")

        # Read the flows.json file
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                flows_data = json.load(file)
        except json.JSONDecodeError:
            # If the file exists but is empty or corrupt, it acts as not found
            raise EnterpriseManagementException("json file not founded")

        # --- NODES 10 & 11: Project ID in json? & Calculate Operations ---
        project_found = False
        total_budget = 0.0

        # Loop through the movements to find our project and calculate
        for entry in flows_data:
            # Trap evasion: check for both uppercase and camelCase keys
            current_id = entry.get("projectID") or entry.get("PROJECT_ID")

            if current_id == project_id:
                project_found = True

                # Sum inflows (handling both "inFlow" and "inflow")
                if "inFlow" in entry:
                    total_budget += float(entry["inFlow"])
                elif "inflow" in entry:
                    total_budget += float(entry["inflow"])

                # Subtract outflows (handling both "outFlow" and "outflow")
                if "outFlow" in entry:
                    total_budget -= float(entry["outFlow"])
                elif "outflow" in entry:
                    total_budget -= float(entry["outflow"])

        # If we finished reading the whole file and didn't find the ID
        if not project_found:
            raise EnterpriseManagementException("Project Id is not registered")

        # --- NODE 12: Operations (Save to output file) ---
        # Create the dictionary with the required fields (ID, UTC timestamp, result)
        output_record = {
            "PROJECT_ID": project_id,
            "date": datetime.now(timezone.utc).timestamp(),
            "result": total_budget
        }

        # The manual says "a json output file", we will use this name
        output_file = "project_budgets.json"

        # Read existing budgets file to not overwrite other projects
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as file:
                try:
                    output_data = json.load(file)
                except json.JSONDecodeError:
                    output_data = []
        else:
            output_data = []

        output_data.append(output_record)

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output_data, file, indent=4)

        # --- NODE 13: END (Return True) ---
        return True

    @staticmethod
    def validate_cif(cif: str) -> bool:
        """
        Validates if a Spanish CIF is mathematically correct.
        """

        # Verify length constraint
        if len(cif) != 9:
            return False

        # Verify the first character against the allowed list of letters
        first_letter = cif[0].upper()
        valid_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if first_letter not in valid_letters:
            return False

        # Extract the central 7 characters and verify they are all digits
        digits = cif[1:8]
        if not digits.isdigit():
            return False

        # Initialize the mapping for the control digit calculation
        control_mapping = "JABCDEFGHI"

        # Sum the digits in the even positions (indices 1, 3, 5)
        even_sum = int(digits[1]) + int(digits[3]) + int(digits[5])

        # Process the digits in the odd positions (indices 0, 2, 4, 6)
        odd_sum = 0
        for i in [0, 2, 4, 6]:
            val = int(digits[i]) * 2
            # Sum the individual digits of the multiplication result
            odd_sum += (val // 10) + (val % 10)

        total = even_sum + odd_sum

        # Calculate the control digit
        control_digit = (10 - (total % 10)) % 10

        expected_number = str(control_digit)
        expected_letter = control_mapping[control_digit]

        # Verify if the last character matches the calculated number or letter
        last_char = cif[8].upper()
        return last_char == expected_number or last_char == expected_letter
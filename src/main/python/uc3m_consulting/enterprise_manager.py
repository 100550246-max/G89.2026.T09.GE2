from src.main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class EnterpriseManager:
    """Class for providing the methods for managing the projects"""

    def __init__(self):
        pass

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

        # Temporary dummy return to keep the method signature valid for TC1
        return "00000000000000000000000000000000"


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
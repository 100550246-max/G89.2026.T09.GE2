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


        #TC2
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("CIF is not a valid string")

        #GENERIC RETURN
        return "00000000000000000000000000000000"

    @staticmethod
    def validate_cif(cif: str):
        """Validates the CIF algorithm"""
        # Esto lo rellenaremos más adelante para el TC3
        return True
import unittest
import json
import os
import shutil
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterDocument(unittest.TestCase):
    def test_valid_pdf_document(self):
        import os
        system = EnterpriseManager()
        file_path = "valid_pdf.json"

        # 1. Creamos el archivo con datos correctos ("Create file with correct data")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('{"PROJECT_ID": "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d", "FILENAME": "testdoc1.pdf"}')

        try:
            # 2. Ejecutamos tu código ("Execute your code")
            result = system.register_document(file_path)

            # 3. Comprobaciones ("Assertions")
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertEqual(len(result), 64)  # El hash SHA-256 siempre tiene 64 caracteres

        finally:
            # 4. Limpieza: Borramos el archivo temporal ("Cleanup: Delete temporary file")
            if os.path.exists(file_path):
                os.remove(file_path)
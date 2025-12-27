import os
import shutil
from fastapi import UploadFile
import uuid

class FileManager:
    """
    Class responsible for handling file uploads and validation.
    """
    UPLOAD_DIR = "uploads"

    def __init__(self):
        if not os.path.exists(self.UPLOAD_DIR):
            os.makedirs(self.UPLOAD_DIR)

    def save_file(self, file: UploadFile) -> str:
        """
        Saves the uploaded file to disk and returns the file path.
        """
        self._validate_file(file)
        
        # Generate a unique filename to avoid collisions
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return file_path

    def _validate_file(self, file: UploadFile):
        """
        Validates the file extension.
        """
        allowed_extensions = {"csv", "tsv", "xlsx", "xls"}
        filename = file.filename
        extension = filename.split(".")[-1].lower()
        
        if extension not in allowed_extensions:
            raise ValueError(f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}")

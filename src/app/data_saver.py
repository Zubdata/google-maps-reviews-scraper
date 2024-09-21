from app.config import Config
from app.communiator import Communicator

import pandas as pd
import os

class DataSaver:
    """This class is responsible for saving structured data in a format selected by user"""

    def save(self, data: list):
        Communicator.log_message("Going to save data")

        df = self.convert_to_dataframe(data)
        file_format = Config.get_format()
        filename = self.generate_unique_filename(file_format)
        self.save_dataframe(df, filename, file_format)

        Communicator.log_message(f"Data saved successfully to {filename}")


    def convert_to_dataframe(self, data: list) -> pd.DataFrame:
        """Convert list of data to a pandas DataFrame."""

        return pd.DataFrame(data)

    def generate_unique_filename(self, file_format: str) -> str:
        """Generate a unique filename based on the format."""

        base_filename = "reviews"
        extension = self.get_file_extension(file_format)
        filename = base_filename + extension
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_filename}_{counter}{extension}"
            counter += 1
        return filename

    def get_file_extension(self, file_format: str) -> str:
        """Return the file extension based on the format."""

        if file_format == "json":
            return ".json"
        elif file_format == "csv":
            return ".csv"
        elif file_format == "excel":
            return ".xlsx"
        else:
            raise ValueError(f"Unsupported format: {file_format}")

    def save_dataframe(self, df: pd.DataFrame, filename: str, file_format: str):
        """Save the DataFrame to a file in the specified format."""
        
        if file_format == "json":
            df.to_json(filename, orient="records", indent=4)
        elif file_format == "csv":
            df.to_csv(filename, index=False)
        elif file_format == "excel":
            df.to_excel(filename, index=False)

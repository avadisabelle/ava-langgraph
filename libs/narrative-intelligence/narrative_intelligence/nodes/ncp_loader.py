"""
🧠 1. NCP Loader Node

A LangGraph node that loads and validates Narrative Context Protocol (NCP) data.
"""

import json
from pathlib import Path
from typing import Union, Dict, Any
from pydantic import ValidationError

from ..schemas import NCPData, NCPState


class NCPLoaderNode:
    """
    Loads and validates NCP data from various sources.

    This node serves as the entry point for NCP analysis graphs, ensuring
    data integrity from the start.
    """

    def __init__(self, validate: bool = True):
        """
        Initialize the NCP Loader Node.

        Args:
            validate: Whether to validate the loaded data against the NCP schema
        """
        self.validate = validate

    def load_from_file(self, file_path: Union[str, Path]) -> NCPData:
        """
        Load NCP data from a JSON file.

        Args:
            file_path: Path to the NCP JSON file

        Returns:
            Validated NCPData object

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
            ValidationError: If the data doesn't conform to the NCP schema
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"NCP file not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return self._validate_data(data)

    def load_from_dict(self, data: Dict[str, Any]) -> NCPData:
        """
        Load NCP data from a dictionary.

        Args:
            data: Dictionary containing NCP data

        Returns:
            Validated NCPData object

        Raises:
            ValidationError: If the data doesn't conform to the NCP schema
        """
        return self._validate_data(data)

    def load_from_url(self, url: str) -> NCPData:
        """
        Load NCP data from a URL.

        Args:
            url: URL to the NCP JSON file

        Returns:
            Validated NCPData object

        Raises:
            ImportError: If requests library is not installed
            requests.RequestException: If the URL cannot be accessed
            ValidationError: If the data doesn't conform to the NCP schema
        """
        try:
            import requests
        except ImportError:
            raise ImportError("requests library is required to load from URL. Install with: pip install requests")

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return self._validate_data(data)

    def _validate_data(self, data: Dict[str, Any]) -> NCPData:
        """
        Validate data against the NCP schema.

        Args:
            data: Dictionary containing NCP data

        Returns:
            Validated NCPData object

        Raises:
            ValidationError: If the data doesn't conform to the NCP schema
        """
        if self.validate:
            try:
                return NCPData(**data)
            except ValidationError as e:
                raise ValidationError(f"NCP data validation failed: {e}")
        else:
            # Even without validation, we still create the object
            # This allows for more lenient parsing
            return NCPData(**data)

    def __call__(self, state: NCPState) -> NCPState:
        """
        LangGraph node callable.

        Expects state to contain either:
        - 'ncp_file_path': Path to NCP JSON file
        - 'ncp_url': URL to NCP JSON file
        - 'ncp_dict': Dictionary containing NCP data

        Args:
            state: Current NCPState

        Returns:
            Updated NCPState with loaded ncp_data
        """
        try:
            if 'ncp_file_path' in state['metadata']:
                ncp_data = self.load_from_file(state['metadata']['ncp_file_path'])
            elif 'ncp_url' in state['metadata']:
                ncp_data = self.load_from_url(state['metadata']['ncp_url'])
            elif 'ncp_dict' in state['metadata']:
                ncp_data = self.load_from_dict(state['metadata']['ncp_dict'])
            else:
                raise ValueError("No NCP data source provided. Specify 'ncp_file_path', 'ncp_url', or 'ncp_dict' in metadata.")

            return {
                **state,
                "ncp_data": ncp_data,
                "error": None,
            }

        except Exception as e:
            return {
                **state,
                "ncp_data": None,
                "error": str(e),
            }

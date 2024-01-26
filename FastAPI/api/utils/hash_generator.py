"""
HashGenerator Class.

This class provides a simple utility for generating SHA-256 hash values for input strings.

Usage:
    - Instantiate the HashGenerator class.
    - Use the 'hash_string' method to hash a given input string.

Example:
    hash_generator = HashGenerator()
    hashed_value = hash_generator.hash_string("example_string")

Note:
    - The class uses the SHA-256 hashing algorithm.
    - The 'hash_string' method updates the internal hash object and returns the hashed string.
"""
import hashlib


class HashGenerator:
    """
    HashGenerator class for generating SHA-256 hash values.
    """

    def __init__(self):
        """
        Constructor method to initialize the HashGenerator.

        Initializes an internal SHA-256 hash object.

        Usage:
            hash_generator = HashGenerator()
        """
        self._hash_object = hashlib.sha256()

    def hash_string(self, input_string):
        """
        Hash a given input string using SHA-256.

        Args:
            input_string (str): The input string to be hashed.

        Returns:
            str: The SHA-256 hashed string.

        Usage:
            hashed_value = hash_generator.hash_string("example_string")
        """
        self._hash_object.update(input_string.encode("utf-8"))
        hashed_string = self._hash_object.hexdigest()
        return hashed_string

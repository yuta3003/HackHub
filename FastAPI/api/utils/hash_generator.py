import hashlib


class HashGenerator:
    def __init__(self):
        self._hash_object = hashlib.sha256()

    def hash_string(self, input_string):
        self._hash_object.update(input_string.encode("utf-8"))
        hashed_string = self._hash_object.hexdigest()
        return hashed_string

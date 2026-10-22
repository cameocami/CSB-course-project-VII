from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import constant_time_compare

class DummyHasher(BasePasswordHasher):
    algorithm = "dummy_hasher"
    def salt(self):
        return "salt"
    def encode(self, password, salt):
        return f"{self.algorithm}${salt}${password}"
    def verify(self, password, encoded):
        try:
            algorithm, salt, hash_val = encoded.split('$', 2)
        except ValueError:
            return False
        return constant_time_compare(self.encode(password, salt), encoded)
    def safe_summary(self, encoded):
        algorithm, salt, password = encoded.split('$', 2)
        return {
            'algorithm': algorithm,
            'salt': salt,
            'hash': password,
        }
    def must_update(self, encoded):
        return False
    def harden_runtime(self, password, encoded):
        pass

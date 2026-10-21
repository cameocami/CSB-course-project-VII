import hashlib
from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.encoding import force_bytes

class DummyHasher(BasePasswordHasher):
    algorithm = "Dummy"
    def salt(self):
        return ""
    def verify(self, password, encoded):
        password = self.encode(password, "salt")
        return password==encoded
    def encode(self, password, salt):
        salt = ""
        password = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()
        return f"{self.algorithm}${salt}${password}"
    def safe_summary(self, encoded):
        return {
            ("algorithm"): self.algorithm,
            ("iterations"): 0,
            ("salt"): self.salt,
            ("hash"): encoded,
        }
    def must_update(self, encoded):
        return False
    def harden_runtime(self, password, encoded):
        pass

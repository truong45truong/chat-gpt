from cryptography.fernet import Fernet, MultiFernet
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property


class FieldCrypto:
    """Encryption Utils."""

    def __init__(self, key):
        super(FieldCrypto, self).__init__()
        self.key = key

    @cached_property
    def keys(self):
        """Get keys for encryption and decryption."""
        key = self.key
        if key is None:
            raise ImproperlyConfigured('Cryptographic key is not properly configured')
        return [Fernet(key=key)]

    @cached_property
    def crypto(self):
        """Get the crypto for encryption and decryption process."""
        return MultiFernet(self.keys)

    @staticmethod
    def generate_key():
        """Generate cryptographic key."""
        return Fernet.generate_key()

    """Do text encryption.
    Args:
        text (str): input text for encryption
    Returns
        encrypted text (str)
    """
    def encrypt(self, text) -> str:
        return self.crypto.encrypt(text.encode('utf-8')).decode('utf-8')

    # Do text decryption.
    # Args:
    #     text (str):
    def decrypt(self, text) -> str:
        return self.crypto.decrypt(text.encode('utf-8')).decode('utf-8')

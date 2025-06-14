
class VigenereCipher:
    """
    Handles simple Vigenère-like encryption and decryption of text.
    This cipher is for educational purposes and is NOT cryptographically secure.
    """
    PRINTABLE_ASCII_START = 32
    PRINTABLE_ASCII_END = 126
    PRINTABLE_ASCII_RANGE_SIZE = PRINTABLE_ASCII_END - PRINTABLE_ASCII_START + 1

    def __init__(self, key: str = "i-see-the-key"):
        """
        Initializes the SimpleVigenereCipher.
        No specific state is stored in this simple version.
        """
        self.key = key
        pass

    def _process_text(self, input_text: str, key: str, encrypt_mode: bool) -> str:
        """
        Internal helper method to process text for encryption or decryption.

        Args:
            input_text (str): The text to be processed (plain text or cipher text).
            key (str): The key for the cipher operation.
            encrypt_mode (bool): True for encryption, False for decryption.

        Returns:
            str: The processed text (cipher text or plain text).
        """
        if not key:

            return input_text

        processed_chars = []
        key_length = len(key)

        for i, text_char_code in enumerate(input_text):
            key_char = key[i % key_length]

            text_ord = ord(text_char_code)
            key_ord = ord(key_char)

            if (self.PRINTABLE_ASCII_START <= text_ord <= self.PRINTABLE_ASCII_END and
                    self.PRINTABLE_ASCII_START <= key_ord <= self.PRINTABLE_ASCII_END):

                shift_amount = key_ord - self.PRINTABLE_ASCII_START

                normalized_text_ord = text_ord - self.PRINTABLE_ASCII_START

                if encrypt_mode:
                    processed_val = (
                        normalized_text_ord + shift_amount) % self.PRINTABLE_ASCII_RANGE_SIZE
                else:

                    processed_val = (normalized_text_ord - shift_amount +
                                     self.PRINTABLE_ASCII_RANGE_SIZE) % self.PRINTABLE_ASCII_RANGE_SIZE

                final_processed_ord = processed_val + self.PRINTABLE_ASCII_START
                processed_chars.append(chr(final_processed_ord))
            else:

                processed_chars.append(text_char_code)

        return "".join(processed_chars)

    def encrypt(self, plain_text: str) -> str:
        """
        Encrypts the plain_text using a Vigenère-like method with the given key.

        Args:
            plain_text (str): The text to be encrypted.
            key (str): The key for encryption.

        Returns:
            str: The encrypted text (ciphertext).
        """
        print("Encrypting text...")
        encrypted_text = self._process_text(plain_text, self.key, True)
        print("Encryption complete.")
        return encrypted_text

    def decrypt(self, cipher_text: str) -> str:
        """
        Decrypts the cipher_text using a Vigenère-like method with the given key.

        Args:
            cipher_text (str): The text to be decrypted.
            key (str): The key used for encryption.

        Returns:
            str: The decrypted text (original plain_text).
        """
        print("Decrypting text...")
        decrypted_text = self._process_text(cipher_text, self.key, False)
        print("Decryption complete.")
        return decrypted_text

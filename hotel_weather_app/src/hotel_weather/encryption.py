import base64
import os

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F


class PIIEncryptor:
    """Encrypts the specified DataFrame columns (AES-GCM), preserving the column names."""

    MODE = "GCM"
    PADDING = "DEFAULT"

    def __init__(self, key_b64: str | None = None):
        key_b64 = key_b64 or os.environ["PII_ENCRYPTION_KEY"]
        key = base64.b64decode(key_b64)
        if len(key) not in (16, 24, 32):
            raise ValueError("The AES key must be 16, 24, or 32 bytes long.")
        self._key_b64 = key_b64

    def __repr__(self) -> str:
        return "PIIEncryptor(key=***)"

    def _key(self) -> Column:
        return F.unbase64(F.lit(self._key_b64))

    @staticmethod
    def _check_columns(df: DataFrame, fields: list[str]) -> None:
        missing = [f for f in fields if f not in df.columns]
        if missing:
            raise ValueError(f"Brak kolumn w DataFrame: {missing}")

    def encrypt(self, df: DataFrame, fields: list[str]) -> DataFrame:
        """Returns a DataFrame in which the specified columns are encrypted (base64)."""
        self._check_columns(df, fields)
        for field in fields:
            encrypted = F.aes_encrypt(
                F.col(field).cast("string"),
                self._key(),
                F.lit(self.MODE),
                F.lit(self.PADDING),
            )
            df = df.withColumn(field, F.base64(encrypted))
        return df

    def decrypt(self, df: DataFrame, fields: list[str]) -> DataFrame:
        """The inverse of encrypt. Primarily for testing and verification."""
        self._check_columns(df, fields)
        for field in fields:
            decrypted = F.aes_decrypt(
                F.unbase64(F.col(field)),
                self._key(),
                F.lit(self.MODE),
                F.lit(self.PADDING),
            )
            df = df.withColumn(field, decrypted.cast("string"))
        return df
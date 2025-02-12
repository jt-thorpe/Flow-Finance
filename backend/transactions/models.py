import enum
import uuid
from typing import Final, Optional

from core.extensions import db
from sqlalchemy import Date, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import text
from transactions.enums import Frequency, TransactionCategory

GEN_RANDOM_UUID: Final[str] = "gen_random_uuid()"
USER_ACCOUNT_ID: Final[str] = "user_account.id"


class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(db.Model):
    """Models a user's financial incomes.

    Attributes:
        id: The UUID of the income.
        user_id: The UUID of the user.
        category: The category of the income.
        date: The date of the income.
        frequency: The frequency of the income.
        amount: The amount of the income in pennies.
        description: A description of the income.

    Relationships:
        user: The user to whom the income belongs.
    """
    __tablename__ = "transaction"

    # Columns
    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey(USER_ACCOUNT_ID),
                                   nullable=False)
    type: TransactionType = db.Column(Enum(TransactionType),
                                      nullable=False)
    category: TransactionCategory = db.Column(Enum(TransactionCategory),
                                              nullable=False)
    date: Date = db.Column(db.Date,
                           nullable=False)
    frequency: Frequency = db.Column(Enum(Frequency),
                                     nullable=True)
    _amount: int = db.Column("amount",
                             db.Integer,
                             nullable=False)
    description: Optional[str] = db.Column(String(100),
                                           nullable=True)

    @hybrid_property
    def amount(self) -> float:
        """Returns amount in pounds."""
        return self._amount / 100

    @amount.setter
    def amount(self, value: float):
        """Stores amount as pence."""
        self._amount = int(round(value * 100))

    # Relationships
    user = db.relationship("User", back_populates="transactions")

    def to_dict(self) -> dict:
        """Convert the instance to a dictionary.

        In the case of "category" and "frequency", the values are converted to their enum values.

        Returns:
            dict: the instance as a dictionary
        """
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "type": self.type.value,
            "category": self.category.value,
            "date": str(self.date),
            "frequency": self.frequency.value if self.frequency else None,
            "amount": self.amount,
            "description": self.description
        }

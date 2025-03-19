import uuid
from typing import Final

from backend.enums.frequency_enums import Frequency
from backend.enums.transaction_enums import TransactionCategory
from backend.extensions import db
from backend.models.transaction_models import Transaction, TransactionType
from sqlalchemy import Enum, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import text

GEN_RANDOM_UUID: Final[str] = "gen_random_uuid()"
USER_ACCOUNT_ID: Final[str] = "user_account.id"


class Budget(db.Model):
    """Models a user's budget for a specific category.

    Attributes:
        id: The UUID of the budget.
        user_id: The UUID of the user.
        category: The category of the budget.
        frequency: The frequency of the budget.
        amount: The amount of the budget in pennies.

    Relationships:
        user: The user to whom the budget belongs.
    """

    __tablename__ = "budget"

    id: uuid.UUID = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=text(GEN_RANDOM_UUID),
    )
    user_id: uuid.UUID = db.Column(ForeignKey(USER_ACCOUNT_ID), nullable=False)
    category: TransactionCategory = db.Column(
        Enum(TransactionCategory), nullable=False, unique=True
    )
    frequency: Frequency = db.Column(Enum(Frequency), nullable=False)
    _amount: int = db.Column("amount", db.Integer, nullable=False)

    user = db.relationship("User", back_populates="budgets")

    @hybrid_property
    def amount(self) -> float:
        """Returns amount in pounds."""
        return self._amount / 100

    @amount.setter
    def amount(self, value: float):
        """Stores amount as pence."""
        self._amount = int(value * 100)

    @hybrid_property
    def spent(self) -> float:
        """Calculates total expenses spent for this budget instance.

        # TODO: Add support for date ranges i.e. a monthly budget only looks at expenses for dates in that month.
        # TODO: Add support for not hitting db everytime, but checking cache first
        """
        return (
            db.session.query(db.func.sum(Transaction._amount))
            .filter(
                Transaction.user_id == self.user_id,
                Transaction.type == TransactionType.EXPENSE,
                Transaction.category == self.category,
            )
            .scalar()
            or 0
        ) / 100

    @hybrid_property
    def remaining(self) -> float:
        """Calculates remaining budget."""
        return self.amount - self.spent

    def to_dict(self) -> dict:
        """Convert the instance to a dictionary.

        In the case of "category" and "frequency", the values are converted to their enum values.

        Returns:
            dict: the instance as a dictionary
        """
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "category": self.category.value,
            "frequency": self.frequency.value if self.frequency else None,
            "amount": self.amount,
            "spent": self.spent,
            "remaining": self.remaining,
        }

import enum


class Frequency(enum.Enum):
    """Represents the possible frequencies of an Income, Expense or Budget."""
    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "Bi-Weekly"
    FOUR_WEEKLY = "Four-Weekly"
    MONTHLY = "Monthly"
    ANNUALLY = "Annually"

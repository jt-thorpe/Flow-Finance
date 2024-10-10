import enum


class Frequency(enum.Enum):
    """Represents the possible frequencies of INCOME or EXPENSE."""
    DAILY = "daily"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi-weekly"
    FOUR_WEEKLY = "4-weekly"
    MONTHLY = "monthly"
    ANNUALLY = "annually"


class ExpenseCategory(enum.Enum):
    """Represents possible categories for a users expenses."""
    RENT = "rent"
    MORTGAGE = "mortgage"
    UTILITIES = "utilities"
    SUBSCRIPTION = "subscription"
    LEISURE = "leisure"
    GROCERIES = "groceries"
    DINING = "dining"
    ALCOHOL = "alcohol"
    HEALTH = "health"
    SPORT = "sport"
    GIGS = "gigs"
    EVENT = "event"


class IncomeCategory(enum.Enum):
    """Represents possible categories for a users income."""
    SALARY = "salary"
    INTEREST = "interest"
    BONUS = "bonus"

import enum


class Frequency(enum.Enum):
    """Represents the possible frequencies of an Income, Expense or Budget."""
    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "Bi-Weekly"
    FOUR_WEEKLY = "Four-Weekly"
    MONTHLY = "Monthly"
    ANNUALLY = "Annually"


class TransactionCategory(enum.Enum):
    """Represents possible categories for a user's transactions."""
    # INCOME
    SALARY = "Salary"
    INTEREST = "Interest"
    BONUS = "Bonus"
    DIVIDEND = "Dividend"
    REFUND = "Refund"
    GIFT = "Gift"

    # EXPENSES
    RENT = "Rent"
    MORTGAGE = "Mortgage"
    UTILITIES = "Utilities"
    SUBSCRIPTION = "Subscription"
    LEISURE = "Leisure"
    GROCERIES = "Groceries"
    DINING = "Dining"
    ALCOHOL = "Alcohol"
    HEALTH = "Health"
    SPORT = "Sport"
    GIGS = "Gigs"
    EVENT = "Event"

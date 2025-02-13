import enum


class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


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

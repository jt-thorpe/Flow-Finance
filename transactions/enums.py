import enum


class Frequency(enum.IntEnum):
    """Represents the possible frequencies of INCOME or EXPENSE."""
    DAILY = 0
    WEEKLY = 1
    BI_WEEKLY = 2
    FOUR_WEEKLY = 3
    MONTHLY = 4
    ANNUALLY = 5

    @property
    def formatted_name(self):
        return self.name.replace("_", " ").capitalize()


class TransactionCategory(enum.IntEnum):
    """Represents possible categories for a user's transactions.

    Integers from 0 to 50 are reserved for EXPENSE categories.
    Integers from 51 to 100 are reserved for INCOME categories.
    """
    # EXPENSES
    RENT = 0
    MORTGAGE = 1
    UTILITIES = 2
    SUBSCRIPTION = 3
    LEISURE = 4
    GROCERIES = 5
    DINING = 6
    ALCOHOL = 7
    HEALTH = 8
    SPORT = 9
    GIGS = 10
    EVENT = 11

    # INCOME
    SALARY = 51
    INTEREST = 52
    BONUS = 53
    DIVIDEND = 54
    REFUND = 55
    GIFT = 56

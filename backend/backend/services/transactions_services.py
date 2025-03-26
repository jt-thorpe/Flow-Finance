from backend.extensions import logger


def paginate_transactions(
    transactions: list, page: int = 1, per_page: int = 20
) -> dict | None:
    """
    Paginate a list of transactions in-memory.

    Args:
        transactions: The full list of transaction dictionaries.
        page: The current page number (1-indexed).
        limit: Number of transactions per page.

    Returns:
        A dictionary containing:
            - 'transactions': The paginated list.
            - 'has_more': A boolean indicating if more items exist beyond this page.
            - 'total': The total number of transactions.
    """
    if not transactions:
        return None

    try:
        total = len(transactions)
        start = (page - 1) * per_page
        end = start + per_page
        paginated = transactions[start:end]
        has_more = end < total

        return {"transactions": paginated, "has_more": has_more, "total": total}
    except ValueError as e:
        logger.error("Unable to paginate transactions.", e)
        raise e

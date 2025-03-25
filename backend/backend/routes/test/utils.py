class DummyDBUser:
    """A dummy class to simulate a DB user record."""

    def to_dict(self):
        """We don't particularly need to check the actual data for these tests,
        but lets return something in the format it would be."""
        return {
            "meta": {"id": "testid", "alias": "testalias"},
            "transactions": [{}, {}, {}],
            "budgets": [{}, {}],
        }


def sim_get_user_cache_hit(monkeypetch, prefix, data):
    """Simulate a cache hit and returned data for get_user_cache."""
    monkeypetch.setattr(f"{prefix}.get_user_cache", lambda user_id: data)


def sim_get_user_cache_miss(monkeypatch, prefix):
    """Simulate a cache miss for get_user_cache."""
    monkeypatch.setattr(
        f"{prefix}.get_user_cache",
        lambda user_id: None,
    )


def sim_get_cache_field_miss(monkeypatch, prefix):
    """Simulate a cache miss for get_user_cache_field."""
    monkeypatch.setattr(
        f"{prefix}.get_user_cache_field",
        lambda user_id, field: None,
    )


def sim_get_user_with_associations_miss(monkeypatch, prefix):
    """Simulate a db miss for get_user_with_associations."""
    monkeypatch.setattr(
        f"{prefix}.get_user_with_associations",
        lambda user_id: None,
    )


def sim_get_user_with_associations_hit(monkeypatch, prefix, data):
    """Simulate a db hit for get_user_with_associations."""
    monkeypatch.setattr(
        f"{prefix}.get_user_with_associations",
        lambda user_id: data,
    )


def sim_cache_user_with_associations_success(monkeypatch, prefix):
    """Simulate successful cache_user_with_associations."""
    monkeypatch.setattr(f"{prefix}.cache_user_with_associations", lambda user: None)


def sim_cache_user_with_associations_fail(monkeypatch, prefix):
    """Simulate successful cache_user_with_associations.

    Fails by throwing an exception.
    """

    def fake_function(*args, **kwargs):
        raise ValueError("Test error")

    monkeypatch.setattr(f"{prefix}.cache_user_with_associations", fake_function)


def sim_add_log_info(monkeypatch, prefix):
    """Simulate adding a INFO log."""
    monkeypatch.setattr(f"{prefix}.logger.info", lambda *args, **kwargs: None)


def sim_add_log_warning(monkeypatch, prefix):
    """Simulate adding a WARNING log."""
    monkeypatch.setattr(f"{prefix}.logger.warning", lambda *args, **kwargs: None)


def sim_add_log_error(monkeypatch, prefix):
    """Simulate adding a ERROR log."""
    monkeypatch.setattr(f"{prefix}.logger.error", lambda *args, **kwargs: None)


def sim_add_log_critical(monkeypatch, prefix):
    """Simulate adding a CRITICAL log."""
    monkeypatch.setattr(f"{prefix}.logger.critical", lambda *args, **kwargs: None)


def sim_compute_dashboard_success(monkeypatch, prefix, data):
    """Sim computing dashboard info successfully."""
    monkeypatch.setattr(f"{prefix}.compute_dashboard", lambda user_data: data)


def sim_compute_dashboard_fail(monkeypatch, prefix):
    """Sim failing to compute dashboard info."""

    def throw_err(*args, **kwargs):
        raise Exception

    monkeypatch.setattr(f"{prefix}.compute_dashboard", throw_err)


def sim_serialise_user_associations_success(monkeypatch, prefix, data):
    """Simulate a successful serialise_user_associations_success."""
    monkeypatch.setattr(f"{prefix}.serialise_user_associations", lambda user: data)


class DummyDashboardData:
    """Represents the returned data for compute dashboard."""

    def to_dict(self):
        """Mimics the structure of the compute_dashboard return."""
        return {
            "user_alias": "test_id",
            "user_latest_transactions": [{}, {}, {}],
            "user_incomes_total": [0, 1, 2],
            "user_expenses_total": [0, 1, 2],
            "user_budget_summary": [{}, {}],
        }

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
    """Simulate a successful cache_user_with_associations."""
    monkeypatch.setattr(
        f"{prefix}.cache_user_with_associations", lambda user_data: None
    )


def sim_serialise_user_associations_success(monkeypatch, prefix, data):
    """Simulate a successful serialise_user_associations_success."""
    monkeypatch.setattr(f"{prefix}.serialise_user_associations", lambda user: data)

import datetime as dt
import json
import logging
import sys

import pytest

from ..logger import MyJSONFormatter, NonErrorFilter


@pytest.fixture
def fmt_keys():
    return {
        "level": "levelname",
        "message": "message",
        "timestamp": "timestamp",
        "logger": "name",
        "module": "module",
        "function": "funcName",
        "line": "lineno",
        "thread_name": "threadName"
    }


@pytest.fixture
def formatter(fmt_keys):
    return MyJSONFormatter(fmt_keys=fmt_keys)


def test_format_basic(formatter):
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=123,
        msg="Hello world",
        args=(),
        exc_info=None,
    )
    record.module = "test_module"
    record.funcName = "test_func"
    record.threadName = "MainThread"

    formatted = formatter.format(record)
    data = json.loads(formatted)

    # Verify keys are mapped correctly using fmt_keys
    assert data["level"] == record.levelname
    assert data["message"] == record.getMessage()
    assert data["logger"] == record.name
    assert data["module"] == record.module
    assert data["function"] == record.funcName
    assert data["line"] == record.lineno
    assert data["thread_name"] == record.threadName

    # Verify that the timestamp is in ISO format
    try:
        dt.datetime.fromisoformat(data["timestamp"])
    except ValueError:
        pytest.fail("Timestamp is not in ISO format")


def test_format_with_extra_attributes(formatter):
    record = logging.LogRecord(
        name="test_logger",
        level=logging.DEBUG,
        pathname="test_path",
        lineno=45,
        msg="Test extra",
        args=(),
        exc_info=None,
    )
    record.module = "test_module"
    record.funcName = "test_func"
    record.threadName = "MainThread"
    # Add an extra attribute not part of the built-in log record fields
    record.extra_info = "extra_value"

    formatted = formatter.format(record)
    data = json.loads(formatted)

    assert "extra_info" in data
    assert data["extra_info"] == "extra_value"


def test_format_with_exception(formatter):
    try:
        raise ValueError("An error occurred")
    except Exception:
        record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname="test_path",
            lineno=78,
            msg="Error message",
            args=(),
            exc_info=sys.exc_info(),
        )
        record.module = "test_module"
        record.funcName = "test_func"
        record.threadName = "MainThread"

        formatted = formatter.format(record)
        data = json.loads(formatted)

        # Check that exc_info is included and is a string
        assert "exc_info" in data
        assert isinstance(data["exc_info"], str)


@pytest.fixture
def non_error_filter():
    return NonErrorFilter()


@pytest.mark.parametrize("level", [logging.DEBUG, logging.INFO])
def test_non_error_filter_allows(non_error_filter, level):
    record = logging.LogRecord(
        name="test_logger",
        level=level,
        pathname="test_path",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None
    )
    assert non_error_filter.filter(record) is True


@pytest.mark.parametrize("level", [logging.WARNING, logging.ERROR, logging.CRITICAL])
def test_non_error_filter_blocks(non_error_filter, level):
    record = logging.LogRecord(
        name="test_logger",
        level=level,
        pathname="test_path",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None
    )
    assert non_error_filter.filter(record) is False

import pytest
import os
import shutil
from christmas_list import ChristmasList

# Path to your empty backup file
EMPTY_DB = "empty_christmas_list.pkl"
REAL_DB = "christmas_list.pkl"

@pytest.fixture(autouse=True)
def clean_database():
    """Run before and after every test: start with empty DB"""
    # Ensure real DB doesn't exist
    if os.path.exists(REAL_DB):
        os.remove(REAL_DB)
    # Copy empty backup to real DB name
    shutil.copy(EMPTY_DB, REAL_DB)
    yield
    # Clean up after test
    if os.path.exists(REAL_DB):
        os.remove(REAL_DB)


def test_add_item():
    cl = ChristmasList(REAL_DB)
    cl.add("Lego Set")
    items = cl.loadItems()
    assert len(items) == 1
    assert items[0]["name"] == "Lego Set"
    assert items[0]["purchased"] is False


def test_check_off_item():
    cl = ChristmasList(REAL_DB)
    cl.add("Bike")
    cl.check_off("Bike")
    items = cl.loadItems()
    assert items[0]["purchased"] is True


def test_check_off_nonexistent_item_does_nothing():
    cl = ChristmasList(REAL_DB)
    cl.add("Book")
    cl.check_off("Ghost Item")  # doesn't exist
    items = cl.loadItems()
    assert len(items) == 1
    assert items[0]["name"] == "Book"


def test_remove_item():
    cl = ChristmasList(REAL_DB)
    cl.add("PlayStation")
    cl.add("Xbox")
    cl.remove("PlayStation")
    items = cl.loadItems()
    assert len(items) == 1
    assert items[0]["name"] == "Xbox"


def test_remove_nonexistent_item_does_nothing():
    cl = ChristmasList(REAL_DB)
    cl.add("Switch")
    cl.remove("Missing")
    items = cl.loadItems()
    assert len(items) == 1


def test_print_list(capsys):
    cl = ChristmasList(REAL_DB)
    cl.add("Gift A")
    cl.add("Gift B")
    cl.check_off("Gift A")
    cl.print_list()
    captured = capsys.readouterr()
    assert "[x] Gift A" in captured.out
    assert "[_] Gift B" in captured.out


def test_multiple_operations_work_together():
    cl = ChristmasList(REAL_DB)
    cl.add("A")
    cl.add("B")
    cl.check_off("A")
    cl.remove("B")
    items = cl.loadItems()
    assert len(items) == 1
    assert items[0]["name"] == "A"
    assert items[0]["purchased"] is True
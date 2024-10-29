"""Conftest file for Faker."""
from typing import List, Dict
import random
from faker import Faker
import pytest

# Initialize Faker
fake = Faker()

# Custom command line option for pytest
def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption("--num_records", action="store", default=0, type=int,
                     help="Number of records to generate using Faker.")

# Fixture to generate fake data
@pytest.fixture(scope='session')
def fake_data(request) -> List[Dict[str, int]]:
    """Generate fake data for calculator operations."""
    num_records = request.config.getoption("--num_records")
    records = []

    for _ in range(num_records):
        operation = random.choice(['add', 'subtract', 'multiply', 'divide'])
        operand1 = fake.random_number(digits=2)

        # Generate operand2; ensure it is non-zero for division
        if operation == 'divide':
            operand2 = random.randint(1, 99)  # Avoid zero
        else:
            operand2 = fake.random_number(digits=2)

        # Generate a fake record for calculator operations
        record = {
            "operation": operation,
            "operand1": operand1,
            "operand2": operand2
        }
        records.append(record)

    return records

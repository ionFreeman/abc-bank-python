from nose.tools import assert_equal, assert_less_equal
import logging;

from abcbank.transaction import Transaction
from datetime import datetime, timedelta


def test_instance_parameters():
    now = datetime.now()
    transaction = Transaction(5)
    assert_less_equal(transaction.date - now, timedelta(milliseconds=1), 'transaction booked at create date')
    assert_equal(transaction.amount, 5, 'transaction reflects specified value of 5')


def test_statement():
    transaction = Transaction(-5)
    logging.info(str(transaction))
    assert_equal('  withdrawal $5.00', str(transaction))
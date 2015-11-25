from nose.tools import assert_almost_equal, assert_equal, assert_raises

from abcbank.account import Account
from abcbank.bank import Bank
from abcbank.transaction import Transaction
from calendar import isleap
from datetime import datetime, timedelta
from math import pow


def test_transactions():
    account = Bank().add_customer('Kavita').open_account('Savings', 5)
    assert_equal([transaction.amount for transaction in account._transactions], [5,])
    account.withdraw(5)
    assert_equal([transaction.amount for transaction in account._transactions], [5, -5,])

def test_statement():
    account = Bank().add_customer('Praveen').open_account('Checking', 5)
    account.withdraw(4)
    assert_equal(account.statement, """
Checking Account
  deposit $5.00
  withdrawal $4.00
Total $1.00
""")


def test_type_constraint():
    assert_raises(StandardError, Account, 'Cheeseburger')

def test_interest():
    account = Bank().add_customer('Penelope').open_account('Maxi Savings')
    account.deposit(5000, datetime.today() - timedelta(2))
    expected_interest = 5000*(pow(1 + 50./365000, 2) - 1)
    assert_almost_equal(expected_interest, account.interest_earned())
    account.withdraw(4000, datetime.today() - timedelta(1))
    # one day of 5 % interest on $5000
    expected_interest = 5000*(pow(1 + 50./365000, 1) - 1)
    # one day of 1 mil interest on $1000
    expected_interest += (1000 + expected_interest)*(pow(1 + 1./365000, 1) - 1)
    # @todo this blows up at midnight, as another day's interest gets added
    assert_almost_equal(expected_interest, account.interest_earned())

    account = Bank().add_customer('Dick').open_account('Maxi Savings')
    account.deposit(5000, datetime.today() - timedelta(16))
    expected_interest = 5000*(pow(1 + 50./365000, 16) - 1)
    assert_almost_equal(expected_interest, account.interest_earned())
    account.withdraw(4000, datetime.today() - timedelta(15))
    # one day of 5 % interest on $5000
    expected_interest = 5000*(pow(1 + 50./365000, 1) - 1)
    # ten days of 1 mil interest on $1000 + earned interest
    expected_interest += (1000 + expected_interest)*(pow(1 + 1./365000, 10) - 1)
    # five days of 5 % interest on $1000 + earned interest
    expected_interest += (1000 + expected_interest)*(pow(1 + 50./365000, 5) - 1)
    assert_almost_equal(expected_interest, account.interest_earned())

    # check interest over one year against the interest function

    one_year_ago = datetime.now() - timedelta(365) # the leap day can cause an error up to about 1/3 %

    checking_account = Bank().add_customer('Xinqi').open_account('Checking', 1000, one_year_ago)
    expected_interest = 1000*(pow(1 + 1./365000, 365) - 1)
    assert_almost_equal(expected_interest, checking_account.interest_earned())

    savings_account = Bank().add_customer('Yong').open_account('Savings', 5000, one_year_ago)
    # one fifth is at 0.001, four-fifths is at 0.002, so 0.0018 is the rate
    expected_interest = 5000*(pow(1 + 1.8/365000, 365) - 1)
    assert_almost_equal(expected_interest, savings_account.interest_earned())




# coding=utf-8
import logging
from nose.tools import assert_equals, assert_almost_equal

from abcbank.bank import Bank

from datetime import datetime, timedelta
from math import pow


def test_customer_summary():
    bank = Bank()
    bank.add_customer('John').open_account('Checking')
    assert_equals("Customer Summary\n - John (1 account)", bank.customer_summary)

def test_interest():
    """
    @todo These tests cannnot go to Production without making them robust to leap years, which you could do simply by
    turning down the precision on assert_almost_equals: keeping the precision would require pretty rococo test code

    """
    bank = Bank()
    one_year_ago = datetime.today() - timedelta(days = 365)
    two_years_ago = one_year_ago - timedelta(days = 365)

    # first customer with checking account
    bank.add_customer("Bill").open_account('Checking', 100.0, two_years_ago) # 10 ¢ interest
    expected_interest = 100* (pow(1 + 1./365000, 730) - 1)
    assert_almost_equal(expected_interest, bank.total_interest_paid)

    # second customer with savings account
    bank.add_customer("Jill").open_account('Savings', 1500.0, one_year_ago) # $2 interest
    expected_interest += 1500 * (pow(1 + (4./3)/365000, 365) - 1)
    assert_almost_equal(expected_interest, bank.total_interest_paid)

    # third customer with maxi savings account
    phil = bank.add_customer("Phil")
    maxi_savings_account = phil.open_account('Maxi Savings', 3000, datetime.today() - timedelta(days = 30))
    expected_interest_plus_30_days_maxi = expected_interest + 3000 * (pow(1 + 50./365000, 30) - 1)
    assert_almost_equal(expected_interest_plus_30_days_maxi, bank.total_interest_paid)

    # third customer's maxi savings account suffers a withdrawal
    maxi_savings_account.withdraw(2000, datetime.today() - timedelta(days = 20))
    # 3000@10 days maxi interest, 1000@10 days mini interest, 1000@10 days maxi interest
    maxi_interest = 3000 * (pow(1 + 50./365000, 10) - 1)
    maxi_interest += (1000 + maxi_interest) * (pow(1 + 1./365000, 10) - 1)
    maxi_interest += (1000 + maxi_interest) * (pow(1 + 50./365000, 10) - 1)
    expected_interest += maxi_interest
    assert_almost_equal(expected_interest, bank.total_interest_paid)

    # third customer has two accounts
    phil.open_account('Checking', 100.0, datetime.today() - timedelta(days = 30))
    expected_interest += 100* (pow(1 + 1./365000, 30) - 1)
    assert_almost_equal(expected_interest, bank.total_interest_paid)
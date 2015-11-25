from nose.tools import assert_equals, assert_raises_regexp

from abcbank.bank     import Bank


def test_statement():
    henry = Bank().add_customer("Henry")
    henry.open_account('Checking', 100)
    henry.open_account('Savings', 4000).withdraw(200.0)
    assert_equals(henry.statement,
                  "Statement for Henry" +
                  "\n\nChecking Account\n  deposit $100.00\nTotal $100.00" +
                  "\n\nSavings Account\n  deposit $4000.00\n  withdrawal $200.00\nTotal $3800.00" +
                  "\n\nTotal In All Accounts $3900.00")


def test_open_account():
    oscar = Bank().add_customer("Oscar")
    oscar.open_account('Savings')
    oscar.open_account('Checking')
    oscar.open_account('Maxi Savings')
    assert_equals(len(oscar.accounts), 3)


def test_transfer():
    holly = Bank().add_customer('Holly')
    holly.open_account('Savings', 2500)
    holly.open_account('Maxi Savings', 3000)
    # blow up if there are insufficient funds in the only account of a type
    assert_raises_regexp(StandardError, r'Insufficient funds: [$]2500.00 available; [$]3000.00 requested'
                         , holly.transfer, 'Savings', 'Checking', 3000)
    second_savings_account = holly.open_account('Savings', 300)
    # blow up if there are insufficient funds in all accounts of a type
    assert_raises_regexp(StandardError, r'Insufficient funds: [$]2800.00 available; [$]3000.00 requested'
                         , holly.transfer, 'Savings', 'Checking', 3000)
    second_savings_account.deposit(200)
    checking_account = holly.transfer('Savings', 'Checking', 3000)
    # Successful transfer into a new account
    assert_equals('''
Checking Account
  deposit $3000.00
Total $3000.00
''', checking_account.statement)
    # Successful transfer into an existing account
    holly.transfer('Maxi Savings', 'Checking', 3000)
    assert_equals('Statement for Holly\n\nSavings Account\n  deposit $2500.00\n  withdrawal $2500.00\nTotal $0.00\n\nMaxi Savings Account\n  deposit $3000.00\n  withdrawal $3000.00\nTotal $0.00\n\nSavings Account\n  deposit $300.00\n  deposit $200.00\n  withdrawal $500.00\nTotal $0.00\n\nChecking Account\n  deposit $3000.00\n  deposit $3000.00\nTotal $6000.00\n\nTotal In All Accounts $6000.00', str(holly))

    # blow up if either the from or two account types are not recognized
    assert_raises_regexp(StandardError, 'Invalid account type Fandango', holly.transfer, 'Fandango', 'Checking', 1)
    assert_raises_regexp(StandardError, 'Invalid account type Fandango', holly.transfer, 'Checking', 'Fandango', 1)


from calendar import isleap
from datetime import date, timedelta
from abcbank.transaction import Transaction


def step(x): return x if x > 0 else 0;



def savings_rate_function_generator(account, tiers=[(0, 0.001), (1000, 0.002)]):
    """
    Generator for interest calculation functions for a savings account. Interest is spread evenly over the days in a year
    @todo determine whether we should be breaking down the interest into twelfths and dividing those over a month

    :param tiers: boundary values for interest rates
    :type tiers: list of boundary, rate tuples, where the rate applies to values above the boundary
    :return:  a closure to calculate a day's interest given a transaction amount
    """
    def savings_rate_function(amount, date):
        tiers.sort()
        balance = account.balance
        interest = 0.
        incremental_interest_rate = 0.
        weighting = 0
        for tier in tiers:
            # @todo should interest be spread evenly over the days in a year
            # or evenly over the months and the days in each month?
            if balance > tier[0]:
                incremental_interest_rate = tier[1] - incremental_interest_rate
                weighting += (balance - tier[0]) * incremental_interest_rate
            else:
                break
        effective_interest_rate = weighting/balance
        days_in_year = 366. if isleap(date.year) else 365.
        return amount * effective_interest_rate/days_in_year

    return savings_rate_function


def checking_rate_function_generator(account, rate=0.001):
    # just use the savings rate function generator with one tier
    return savings_rate_function_generator(account, [(0, rate),])


def maxi_savings_rate_function_generator(account, usual_rate=0.05, for_span=timedelta(days=10), lowered_rate=0.001):
    """

    :rtype: float
    """

    def maxi_savings_rate_function(amount, date):
        days_in_year = 366. if isleap(date.year) else 365.
        # check for withdrawals trailing the interest date by less than the specified time frame
        if [transaction for transaction in account._transactions if
            transaction.amount < 0 and transaction.date.date() <= date and transaction.date.date() > date - for_span]:
            rate = lowered_rate
        else:
            rate = usual_rate
        return amount * rate / days_in_year

    return maxi_savings_rate_function


rate_generator_by_account_type = {
    'Savings': savings_rate_function_generator
    , 'Checking': checking_rate_function_generator
    , 'Maxi Savings': maxi_savings_rate_function_generator
}


class Account:
    """
    An Account is a list of transactions with a particular interest function generator
    @todo Negative balances should probably incur some penalty
    """

    def __init__(self, account_type):
        if account_type not in rate_generator_by_account_type:
            raise StandardError('Unkown account type {account_type}'.format(account_type=account_type))
        self._transactions = []
        self.account_type = account_type
        self.rate_function = rate_generator_by_account_type[account_type](self)

    def __str__(self):
        transaction_litany = "\n".join([str(transaction) for transaction in self._transactions])
        total_summary = "Total ${:1.2f}".format(sum([t.amount for t in self._transactions]))
        return '''
{account_type} Account
{transaction_litany}
{total_summary}
'''.format(account_type=self.account_type, transaction_litany=transaction_litany, total_summary=total_summary)

    @property
    def balance(self):
        return sum([transaction.amount for transaction in self._transactions])

    def append_transaction(self, amount, date = None):
        self._transactions.append(Transaction(amount, self.rate_function, date))

    def deposit(self, amount, date = None):
        if (amount <= 0):   raise ValueError("amount must be greater than zero")
        self.append_transaction(amount, date)

    def withdraw(self, amount, date = None):
        if (amount <= 0):   raise ValueError("amount must be greater than zero")
        self.append_transaction(-amount, date)

    def interest_earned(self, end_date = None):
        """
        :param end_date: fix the date so crossing midnight while iterating doesn't break us
        :type end_date: datetime.date
        :return: interest earned on account through the specified date
        """
        return sum([transaction.interest(end_date if end_date else date.today()) for transaction in self._transactions])

    @property
    def statement(self):
        return str(self)

from datetime import datetime, date, timedelta


class Transaction(object):
    """
    A Transaction is an amount of money at a time that accrues according to a closure
    """

    def __init__(self, amount, interest_function = lambda y, z: 0, date=None):
        """

        :param amount: Value of transaction -- positive for deposits, negative for withdrawals
        :param interest_function: function that returns an amount of interest given a balance and a date. Defaults to returning 0
        :type interest_function: function
        :param date: effective date of transaction from which interest is calculated
        :type date: datetime.datetime
        :return:
        """
        self.amount = amount
        self.date = date if date else datetime.now()
        self.interest_function = interest_function

    def __str__(self):
        return "  {withdrawal_or_deposit} {amount}".format(
            withdrawal_or_deposit='withdrawal' if self.amount < 0 else 'deposit'
            , amount="${:1.2f}".format(abs(self.amount)))


    def __repr__(self):
        return '{str} at {date}'.format(str=str(self).strip(), date=self.date)


    def interest(self, end_date = None):
        """
        Calculates the transaction's compound interest by applying the account's interest function to this transaction
        from the transaction date to the prior date (ie, not today)

        :param end_date: date through which to calculate interest
        :type end_date: datetime.date
        :return: interest payable due to this transaction
        """
        balance = self.amount
        # range give an empty list for any negative number, so we don't have to compare end_date to self.date
        '''
        This was an unexpected little Python 3 change
        'end_date if end_date else date.today() - self.date.date()' from my Python 2.7 code now gets interpreted as
        'end_date if end_date else (date.today() - self.date.date())', which of course breaks this. So, now I have
        '(end_date if end_date else date.today()) - self.date.date()'
        '''
        for delta in range(((end_date if end_date else date.today()) - self.date.date()).days):
            balance += self.interest_function(balance, self.date.date() + timedelta(days = delta))
        return balance - self.amount
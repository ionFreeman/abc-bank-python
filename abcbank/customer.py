from abcbank.account import Account, rate_generator_by_account_type


class Customer:
    '''
    A Customer is a list of Accounts with a Name
    '''

    def __init__(self, name):
        self.accounts = []
        self.name = name

    def __str__(self):
        statement = "Statement for %s\n" % self.name
        for account in self.accounts:
            statement = '%s%s' % (statement, account)
        statement = '''{0:s}
Total In All Accounts ${1:1.2f}'''.format(statement
                                          , sum([sum([transaction.amount for transaction in account._transactions])
                                                 for account in self.accounts]))
        return statement

    def open_account(self, account_type, initial_transaction_amount=0, initial_transaction_date = None):
        """

        :type initial_transaction_amount: float
        """
        account = Account(account_type)
        self.accounts.append(account)
        if initial_transaction_amount > 0:
            account.deposit(initial_transaction_amount, initial_transaction_date)
        elif initial_transaction_amount < 0:
            account.withdraw(-initial_transaction_amount, initial_transaction_date)
        return account

    def transfer(self, from_account_type, to_account_type, amount):
        '''
        Go through accounts of a particular type, finding enough money to cover the transfer. Move that money to an
        abitrary customer account of the specified account type, creating a new account if required

        :param from_account_type: Account type to debit
        :param to_account_type: Account type to credit
        :param amount: Amount
        :except: StandardError with message 'Insufficient funds: ${balance:f1.2} available; ${request:f1.2} requested'
        :except: AttributeError with message 'Invalid account type {account_type}'
        :return: credited account
        '''
        for account_type in (from_account_type, to_account_type):
            if account_type not in rate_generator_by_account_type:
                raise StandardError('Invalid account type {account_type}'.format(account_type=account_type))
        available = sum([account.balance for account in self.accounts if account.account_type == from_account_type])
        if available < amount:
            raise StandardError(
                'Insufficient funds: ${available:1.2f} available; ${amount:1.2f} requested'.format(
                    available=available, amount=amount))
        remaining = amount
        for account in [acct for acct in self.accounts if acct.account_type == from_account_type]:
            if account.balance >= remaining:
                account.withdraw(remaining)
                remaining = 0
                break
            else:
                remaining -= account.balance
                account.withdraw(account.balance)
        if to_account_type in [acct.account_type for acct in self.accounts]:
            account = [acct for acct in self.accounts if acct.account_type == to_account_type][0]
        else:
            account = self.open_account(to_account_type)
        account.deposit(amount)
        return account

    @property
    def statement(self):
        return str(self)

from datetime import date

from abcbank.customer import Customer

class Bank:
    '''
    A Bank is a list of Customers
    '''
    def __init__(self):
        self.customers = []

    def add_customer(self, customer_name):
        customer = Customer(customer_name)
        self.customers.append(customer)
        return customer

    @property
    def customer_summary(self):
        summary = "Customer Summary"
        for customer in self.customers:
            summary = """{summary}
 - {customer_name} ({account_count} account{s})""".format(summary = summary
            , customer_name = customer.name
            , account_count =  len(customer.accounts)
            , s = 's' if len(customer.accounts) - 1 else '')
        return summary

    @property
    def total_interest_paid(self, end_date = None):
        if end_date is None:
            end_date = date.today()
        return sum(sum([account.interest_earned(end_date)
                        for account in customer.accounts]) for customer in self.customers)

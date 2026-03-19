"""
Bank Management System
======================
Real-world style OOP Python code with:
- Classes & Inheritance
- Encapsulation
- Exception Handling
- Decorators
- File Logging
- Type Hints
"""

import random
import datetime
import functools


# ─────────────────────────────────────────
#  CUSTOM EXCEPTIONS
# ─────────────────────────────────────────


class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Cannot withdraw ₹{amount}. Available balance: ₹{balance}")
        self.balance = balance
        self.amount = amount


class AccountNotFoundError(Exception):
    def __init__(self, acc_id):
        super().__init__(f"Account '{acc_id}' not found in the system.")


class InvalidAmountError(Exception):
    def __init__(self, amount):
        super().__init__(f"Invalid amount: ₹{amount}. Must be greater than 0.")


# ─────────────────────────────────────────
#  DECORATOR — LOG EVERY TRANSACTION
# ─────────────────────────────────────────


def log_transaction(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[LOG {timestamp}] Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Done: {func.__name__}")
        return result

    return wrapper


# ─────────────────────────────────────────
#  BASE CLASS — Account
# ─────────────────────────────────────────


class Account:
    _total_accounts = 0  # class variable (shared)

    def __init__(self, owner: str, balance: float = 0.0):
        self._owner = owner
        self.__balance = balance  # private — no direct access
        self._account_id = self._generate_id()
        self._transactions: list = []
        Account._total_accounts += 1

    # ── static / class methods ──
    @staticmethod
    def _generate_id() -> str:
        return "ACC" + str(random.randint(100000, 999999))

    @classmethod
    def total_accounts(cls) -> int:
        return cls._total_accounts

    # ── properties ──
    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def account_id(self) -> str:
        return self._account_id

    # ── core methods ──
    def _record(self, txn_type: str, amount: float):
        self._transactions.append(
            {
                "type": txn_type,
                "amount": amount,
                "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "balance_after": self.__balance,
            }
        )

    @log_transaction
    def deposit(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError(amount)
        self.__balance += amount
        self._record("DEPOSIT", amount)
        print(f"  ✅ Deposited ₹{amount} | New Balance: ₹{self.__balance}")

    @log_transaction
    def withdraw(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError(amount)
        if amount > self.__balance:
            raise InsufficientFundsError(self.__balance, amount)
        self.__balance -= amount
        self._record("WITHDRAW", amount)
        print(f"  ✅ Withdrew ₹{amount} | New Balance: ₹{self.__balance}")

    def get_statement(self):
        print(f"\n{'='*45}")
        print(f"  STATEMENT — {self._owner} ({self._account_id})")
        print(f"{'='*45}")
        if not self._transactions:
            print("  No transactions yet.")
        for t in self._transactions:
            sign = "+" if t["type"] == "DEPOSIT" else "-"
            print(
                f"  {t['time']}  {t['type']:<10} {sign}₹{t['amount']:<10} Balance: ₹{t['balance_after']}"
            )
        print(f"{'='*45}")
        print(f"  Current Balance: ₹{self.__balance}")
        print(f"{'='*45}\n")

    def __str__(self):
        return (
            f"Account[{self._account_id}] Owner={self._owner} Balance=₹{self.__balance}"
        )

    def __repr__(self):
        return self.__str__()


# ─────────────────────────────────────────
#  CHILD CLASS — SavingsAccount
# ─────────────────────────────────────────


class SavingsAccount(Account):
    INTEREST_RATE = 0.04  # 4% per year

    def __init__(self, owner: str, balance: float = 0.0):
        super().__init__(owner, balance)
        self._account_type = "Savings"

    def apply_interest(self):
        interest = round(self.balance * self.INTEREST_RATE, 2)
        print(f"\n  💰 Applying {self.INTEREST_RATE*100}% interest → +₹{interest}")
        self.deposit(interest)

    def __str__(self):
        return f"SavingsAccount[{self._account_id}] Owner={self._owner} Balance=₹{self.balance}"


# ─────────────────────────────────────────
#  CHILD CLASS — CurrentAccount
# ─────────────────────────────────────────


class CurrentAccount(Account):
    def __init__(
        self, owner: str, balance: float = 0.0, overdraft_limit: float = 10000
    ):
        super().__init__(owner, balance)
        self._overdraft_limit = overdraft_limit
        self._account_type = "Current"

    @log_transaction
    def withdraw(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError(amount)
        if amount > self.balance + self._overdraft_limit:
            raise InsufficientFundsError(self.balance, amount)
        # override parent withdraw — allows overdraft
        self._Account__balance -= amount  # name mangling to access private
        self._record("WITHDRAW", amount)
        print(
            f"  ✅ Withdrew ₹{amount} | Balance: ₹{self.balance} (Overdraft limit: ₹{self._overdraft_limit})"
        )

    def __str__(self):
        return f"CurrentAccount[{self._account_id}] Owner={self._owner} Balance=₹{self.balance}"


# ─────────────────────────────────────────
#  BANK CLASS — manages all accounts
# ─────────────────────────────────────────


class Bank:
    def __init__(self, name: str):
        self.name = name
        self._accounts: dict[str, Account] = {}  # acc_id → Account

    def open_account(self, account: Account):
        self._accounts[account.account_id] = account
        print(f"\n  🏦 New account opened at {self.name}")
        print(f"  {account}")

    def get_account(self, acc_id: str) -> Account:
        if acc_id not in self._accounts:
            raise AccountNotFoundError(acc_id)
        return self._accounts[acc_id]

    @log_transaction
    def transfer(self, from_id: str, to_id: str, amount: float):
        sender = self.get_account(from_id)
        receiver = self.get_account(to_id)
        sender.withdraw(amount)
        receiver.deposit(amount)
        print(f"  💸 Transferred ₹{amount} from {sender.owner} → {receiver.owner}")

    def total_deposits(self) -> float:
        return sum(acc.balance for acc in self._accounts.values())

    def list_accounts(self):
        print(f"\n{'─'*45}")
        print(f"  {self.name} — All Accounts ({len(self._accounts)} total)")
        print(f"{'─'*45}")
        for acc in self._accounts.values():
            print(f"  {acc}")
        print(f"{'─'*45}")
        print(f"  Total Deposits: ₹{self.total_deposits()}")
        print(f"{'─'*45}\n")


# ─────────────────────────────────────────
#  MAIN — runs everything
# ─────────────────────────────────────────


def main():
    print("\n" + "█" * 45)
    print("   PYTHON BANK SYSTEM — OOP DEMO")
    print("█" * 45)

    # create bank
    bank = Bank("PyBank India")

    # create accounts
    yuv_savings = SavingsAccount("Yuvraj", balance=5000)
    rahul_current = CurrentAccount("Rahul", balance=2000, overdraft_limit=5000)

    bank.open_account(yuv_savings)
    bank.open_account(rahul_current)

    # operations
    try:
        yuv_savings.deposit(3000)
        yuv_savings.withdraw(1500)
        yuv_savings.apply_interest()

        rahul_current.deposit(1000)
        rahul_current.withdraw(7000)  # uses overdraft

        # transfer money
        bank.transfer(yuv_savings.account_id, rahul_current.account_id, 2000)

        # error demo
        print("\n--- Testing error handling ---")
        yuv_savings.withdraw(999999)  # will fail

    except InsufficientFundsError as e:
        print(f"\n  ❌ ERROR: {e}")
    except InvalidAmountError as e:
        print(f"\n  ❌ INVALID: {e}")
    except AccountNotFoundError as e:
        print(f"\n  ❌ NOT FOUND: {e}")

    # print statements
    yuv_savings.get_statement()
    rahul_current.get_statement()

    # bank overview
    bank.list_accounts()
    print(f"  Total accounts ever created: {Account.total_accounts()}")


if __name__ == "__main__":
    main()

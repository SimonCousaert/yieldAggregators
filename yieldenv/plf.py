from dataclasses import dataclass
import dataclasses
import logging
import numpy as np

class User:
    def __init__(self, name: str):
        self.user_collected_tokens = 0
        self.user_deposit_available_as_collateral = 0
        self.user_interest_revenue = 0
        self.user_paid_interest = 0
        self.name = name

    def getProfit(self, token_price):

        fees = self.user_interest_revenue - self.user_paid_interest
        tokens = self.user_collected_tokens
        value = tokens * token_price

        return (
            "Collected fees (in supplied token): "
            + str(fees)
            + ". Collected tokens: "
            + str(tokens)
            + ", worth: "
            + str(value)
        )


class Plf:
    def __init__(
        self,
        supply_apr: float,
        borrow_apr: float,
        distribution_per_day: float,
        total_available_funds: float = 100,
        collateral_ratio: float = 1.2,
    ):
        self.supply_apr = supply_apr
        self.borrow_apr = borrow_apr
        self.total_available_funds = total_available_funds
        self.collateral_ratio = (
            collateral_ratio
            # collateral divided by amount able to borrow
        )
        self.distribution_per_day = distribution_per_day
        

    def supply(self, amount, days, user: User):

        self.total_available_funds += amount
        user.user_interest_revenue += amount * (self.supply_apr / 365) * days

        user.user_deposit_available_as_collateral += amount

        user.user_collected_tokens += (
            amount / self.total_available_funds * self.distribution_per_day * days
        )  # this assumes that the portion of supplied tokens is constant throughout the supplying period

    def borrow(self, amount: float, days: float, user: User):
        collateral = amount * self.collateral_ratio
        assert (
            self.user_deposit_available_as_collateral >= collateral
        ), "Borrow position under-collateralized"

        # self.user_deposit_available_as_collateral -= amount
        self.total_available_funds -= amount

        user.user_paid_interest += amount * (self.borrow_apr / 365) * days

        user.deposit_available_as_collateral -= amount
        user.collected_tokens += (
            amount / self.total_available_funds * self.distribution_per_day * days
        )  # this assumes that the portion of supplied tokens is constant throughout the supplying period

    def supply_then_borrow(self, amount, days):
        collateral = amount * self.collateral_ratio
        self.supply(amount=collateral, days=days)
        self.borrow(amount=amount, days=days)
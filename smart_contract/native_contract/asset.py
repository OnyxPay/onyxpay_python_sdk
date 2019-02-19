#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
from time import time

from ontology.utils import util
from ontology.common.define import *
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.common.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.vm.build_vm import build_native_invoke_code


class Asset(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    @staticmethod
    def get_asset_address(asset: str) -> bytearray:
        """
        This interface is used to get the ONT or ONG asset's address.

        :param asset: a string which is used to indicate which asset's address we want to get.
        :return: asset's address in the form of bytearray.
        """
        if asset.upper() == 'ONT':
            contract_address = ONT_CONTRACT_ADDRESS
        elif asset.upper() == 'ONG':
            contract_address = ONG_CONTRACT_ADDRESS
        else:
            raise ValueError("asset is not equal to ONT or ONG")
        return contract_address

    def query_balance(self, asset: str, b58_address: str) -> int:
        """
        This interface is used to query the account's ONT or ONG balance.

        :param asset: a string which is used to indicate which asset we want to check the balance.
        :param b58_address: a base58 encode account address.
        :return: account balance.
        """
        raw_address = Address.b58decode(b58_address).to_array()
        contract_address = util.get_asset_address(asset)
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "balanceOf", raw_address)
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        version = 0
        tx_type = 0xd1
        gas_price = 0
        gas_limit = 0
        attributes = bytearray()
        signers = list()
        hash_value = bytearray()
        tx = Transaction(version, tx_type, unix_time_now, gas_price, gas_limit, payer, invoke_code, attributes, signers,
                         hash_value)
        balance = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        array = bytearray(binascii.a2b_hex(balance.encode('ascii')))
        array.reverse()
        try:
            balance = int(binascii.b2a_hex(array).decode('ascii'), 16)
        except ValueError:
            balance = 0
        return balance

    def query_allowance(self, asset: str, b58_from_address: str, b58_to_address: str) -> int:
        """

        :param asset: a string which is used to indicate which asset's allowance we want to get.
        :param b58_from_address: a base58 encode address which indicate where the allowance from.
        :param b58_to_address: a base58 encode address which indicate where the allowance to.
        :return: the amount of allowance in the from of int.
        """
        contract_address = util.get_asset_address(asset)
        raw_from = Address.b58decode(b58_from_address).to_array()
        raw_to = Address.b58decode(b58_to_address).to_array()
        args = {"from": raw_from, "to": raw_to}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "allowance", args)
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        version = 0
        tx_type = 0xd1
        gas_price = 0
        gas_limit = 0
        attributes = bytearray()
        signers = list()
        hash_value = bytearray()
        tx = Transaction(version, tx_type, unix_time_now, gas_price, gas_limit, payer, invoke_code, attributes, signers,
                         hash_value)
        allowance = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        array = bytearray(binascii.a2b_hex(allowance.encode('ascii')))
        array.reverse()
        try:
            allowance = int(binascii.b2a_hex(array).decode('ascii'), 16)
        except ValueError:
            allowance = 0
        return allowance

    def query_unbound_ong(self, base58_address: str) -> int:
        """
        This interface is used to query the amount of account's unbound ong.

        :param base58_address: a base58 encode address which indicate which account's unbound ong we want to query.
        :return: the amount of unbound ong in the form of int.
        """
        contract_address = util.get_asset_address('onyx')
        result = self.__sdk.rpc.get_allowance("oxg", Address(contract_address).b58encode(), base58_address)
        return int(result)

    def query_name(self, asset: str) -> str:
        """
        This interface is used to query the asset's name of ONT or ONG.

        :param asset: a string which is used to indicate which asset's name we want to get.
        :return: asset's name in the form of string.
        """
        contract_address = util.get_asset_address(asset)
        method = 'name'
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), method, bytearray())
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        version = 0
        tx_type = 0xd1
        gas_price = 0
        gas_limit = 0
        attributes = bytearray()
        signers = list()
        hash_value = bytearray()
        tx = Transaction(version, tx_type, unix_time_now, gas_price, gas_limit, payer, invoke_code, attributes, signers,
                         hash_value)
        res = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return bytes.fromhex(res).decode()

    def query_symbol(self, asset: str) -> str:
        """
        This interface is used to query the asset's symbol of ONT or ONG.

        :param asset: a string which is used to indicate which asset's symbol we want to get.
        :return: asset's symbol in the form of string.
        """
        contract_address = util.get_asset_address(asset)
        method = 'symbol'
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), method, bytearray())
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        version = 0
        tx_type = 0xd1
        gas_price = 0
        gas_limit = 0
        attributes = bytearray()
        signers = list()
        hash_value = bytearray()
        tx = Transaction(version, tx_type, unix_time_now, gas_price, gas_limit, payer, invoke_code, attributes, signers,
                         hash_value)
        res = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return bytes.fromhex(res).decode()

    def query_decimals(self, asset: str) -> int:
        """
        This interface is used to query the asset's decimals of ONT or ONG.

        :param asset: a string which is used to indicate which asset's decimals we want to get
        :return: asset's decimals in the form of int
        """
        contract_address = util.get_asset_address(asset)
        method = 'decimals'
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), method, bytearray())
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        version = 0
        tx_type = 0xd1
        gas_price = 0
        gas_limit = 0
        attributes = bytearray()
        signers = list()
        hash_value = bytearray()
        tx = Transaction(version, tx_type, unix_time_now, gas_price, gas_limit, payer, invoke_code, attributes, signers,
                         hash_value)
        decimal = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return int(decimal)

    @staticmethod
    def new_transfer_transaction(asset: str, b58_from_address: str, b58_to_address: str, amount: int,
                                 b58_payer_address: str, gas_limit: int, gas_price: int) -> Transaction:
        """
        This interface is used to generate a Transaction object for transfer.

        :param asset: a string which is used to indicate which asset we want to transfer.
        :param b58_from_address: a base58 encode address which indicate where the asset from.
        :param b58_to_address: a base58 encode address which indicate where the asset to.
        :param amount: the amount of asset that will be transferred.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which can be used for transfer.
        """
        if not isinstance(b58_from_address, str) or not isinstance(b58_to_address, str) or not isinstance(
                b58_payer_address, str):
            raise SDKException(ErrorCode.param_err('the data type of base58 encode address should be the string.'))
        if len(b58_from_address) != 34 or len(b58_to_address) != 34 or len(b58_payer_address) != 34:
            raise SDKException(ErrorCode.param_err('the length of base58 encode address should be 34 bytes.'))
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('the gas price should be equal or greater than zero.'))
        if gas_limit < 0:
            raise SDKException(ErrorCode.other_error('the gas limit should be equal or greater than zero.'))
        contract_address = util.get_asset_address(asset)
        raw_from = Address.b58decode(b58_from_address).to_array()
        raw_to = Address.b58decode(b58_to_address).to_array()
        raw_payer = Address.b58decode(b58_payer_address).to_array()
        state = [{"from": raw_from, "to": raw_to, "amount": amount}]
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "transfer", state)
        unix_time_now = int(time())
        version = 0
        tx_type = 0xd1
        attributes = bytearray()
        signers = list()
        hash_value = bytearray()
        return Transaction(version, tx_type, unix_time_now, gas_price, gas_limit, raw_payer, invoke_code, attributes,
                           signers, hash_value)

    @staticmethod
    def new_approve_transaction(asset: str, b58_send_address: str, b58_recv_address: str, amount: int,
                                b58_payer_address: str, gas_limit: int, gas_price: int) -> Transaction:
        """
        This interface is used to generate a Transaction object for approve.

        :param asset: a string which is used to indicate which asset we want to approve.
        :param b58_send_address: a base58 encode address which indicate where the approve from.
        :param b58_recv_address: a base58 encode address which indicate where the approve to.
        :param amount: the amount of asset that will be approved.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which can be used for approve.
        """
        if not isinstance(b58_send_address, str) or not isinstance(b58_recv_address, str):
            raise SDKException(ErrorCode.param_err('the data type of base58 encode address should be the string.'))
        if len(b58_send_address) != 34 or len(b58_recv_address) != 34:
            raise SDKException(ErrorCode.param_err('the length of base58 encode address should be 34 bytes.'))
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('the gas price should be equal or greater than zero.'))
        if gas_limit < 0:
            raise SDKException(ErrorCode.other_error('the gas limit should be equal or greater than zero.'))
        contract_address = util.get_asset_address(asset)
        raw_send = Address.b58decode(b58_send_address).to_array()
        raw_recv = Address.b58decode(b58_recv_address).to_array()
        raw_payer = Address.b58decode(b58_payer_address).to_array()
        args = {"from": raw_send, "to": raw_recv, "amount": amount}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "approve", args)
        unix_time_now = int(time())
        return Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, raw_payer, invoke_code, bytearray(), [],
                           bytearray())

    @staticmethod
    def new_transfer_from_transaction(asset: str, b58_send_address: str, b58_from_address: str, b58_recv_address: str,
                                      amount: int, b58_payer_address: str, gas_limit: int,
                                      gas_price: int) -> Transaction:
        """
        This interface is used to generate a Transaction object that allow one account to transfer
        a amount of ONT or ONG Asset to another account, in the condition of the first account had been approved.

        :param asset: a string which is used to indicate which asset we want to transfer.
        :param b58_send_address: a base58 encode address which indicate where the asset from.
        :param b58_from_address: a base58 encode address which indicate where the asset from.
        :param b58_recv_address: a base58 encode address which indicate where the asset to.
        :param amount: the amount of asset that will be transferred.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which allow one account to transfer a amount of asset to another account.
        """
        raw_sender = Address.b58decode(b58_send_address).to_array()
        raw_from = Address.b58decode(b58_from_address).to_array()
        raw_to = Address.b58decode(b58_recv_address).to_array()
        raw_payer = Address.b58decode(b58_payer_address).to_array()
        contract_address = util.get_asset_address(asset)
        args = {"sender": raw_sender, "from": raw_from, "to": raw_to, "amount": amount}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "transferFrom", args)
        unix_time_now = int(time())
        return Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, raw_payer, invoke_code, bytearray(), [],
                           bytearray())

    @staticmethod
    def new_withdraw_ong_transaction(b58_claimer_address: str, b58_recv_address: str, amount: int,
                                     b58_payer_address: str, gas_limit: int, gas_price: int) -> Transaction:
        """
        This interface is used to generate a Transaction object that
        allow one account to withdraw an amount of ong and transfer them to receive address.

        :param b58_claimer_address: a base58 encode address which is used to indicate who is the claimer.
        :param b58_recv_address: a base58 encode address which is used to indicate who receive the claimed ong.
        :param amount: the amount of asset that will be claimed.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which can be used for withdraw ong.
        """
        if not isinstance(b58_claimer_address, str) or not isinstance(b58_recv_address, str) or not isinstance(
                b58_payer_address, str):
            raise SDKException(ErrorCode.param_err('the data type of base58 encode address should be the string.'))
        if len(b58_claimer_address) != 34 or len(b58_recv_address) != 34 or len(b58_payer_address) != 34:
            raise SDKException(ErrorCode.param_err('the length of base58 encode address should be 34 bytes.'))
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('the gas price should be equal or greater than zero.'))
        if gas_limit < 0:
            raise SDKException(ErrorCode.other_error('the gas limit should be equal or greater than zero.'))
        ont_contract_address = util.get_asset_address('onyx')
        ong_contract_address = util.get_asset_address("oxg")
        args = {"sender": Address.b58decode(b58_claimer_address).to_array(), "from": ont_contract_address,
                "to": Address.b58decode(b58_recv_address).to_array(), "value": amount}
        invoke_code = build_native_invoke_code(ong_contract_address, bytes([0]), "transferFrom", args)
        unix_time_now = int(time())
        payer_array = Address.b58decode(b58_payer_address).to_array()
        return Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_array, invoke_code, bytearray(), [],
                           bytearray())

    def send_transfer(self, asset: str, from_acct: Account, b58_to_address: str, amount: int, payer: Account,
                      gas_limit: int, gas_price: int):
        """
        This interface is used to send a transfer transaction that only for ONT or ONG.

        :param asset: a string which is used to indicate which asset we want to transfer.
        :param from_acct: a Account object which indicate where the asset from.
        :param b58_to_address: a base58 encode address which indicate where the asset to.
        :param amount: the amount of asset that will be transferred.
        :param payer: a Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: hexadecimal transaction hash value.
        """
        tx = Asset.new_transfer_transaction(asset, from_acct.get_address_base58(), b58_to_address, amount,
                                            payer.get_address_base58(), gas_limit, gas_price)
        self.__sdk.sign_transaction(tx, from_acct)
        if from_acct.get_address_base58() != payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        return self.__sdk.rpc.send_raw_transaction(tx)

    def send_withdraw_ong_transaction(self, claimer: Account, b58_recv_address: str, amount: int, payer: Account,
                                      gas_limit: int, gas_price: int) -> str:
        """
        This interface is used to withdraw a amount of ong and transfer them to receive address.

        :param claimer: the owner of ong that remained to claim.
        :param b58_recv_address: the address that received the ong.
        :param amount: the amount of ong want to claim.
        :param payer: an Account class that used to pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: hexadecimal transaction hash value.
        """
        if claimer is None:
            raise SDKException(ErrorCode.param_err('the claimer should not be None.'))
        if payer is None:
            raise SDKException(ErrorCode.param_err('the payer should not be None.'))
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('the gas price should be equal or greater than zero.'))
        if gas_limit < 0:
            raise SDKException(ErrorCode.other_error('the gas limit should be equal or greater than zero.'))
        b58_claimer = claimer.get_address_base58()
        b58_payer = payer.get_address_base58()
        tx = Asset.new_withdraw_ong_transaction(b58_claimer, b58_recv_address, amount, b58_payer, gas_limit, gas_price)
        tx = self.__sdk.sign_transaction(tx, claimer)
        if claimer.get_address_base58() != payer.get_address_base58():
            tx = self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def send_approve(self, asset, sender: Account, b58_recv_address: str, amount: int, payer: Account, gas_limit: int,
                     gas_price: int) -> str:
        """
        This is an interface used to send an approve transaction
        which allow receiver to spend a amount of ONT or ONG asset in sender's account.

        :param asset: a string which is used to indicate what asset we want to approve.
        :param sender: an Account class that send the approve transaction.
        :param b58_recv_address: a base58 encode address which indicate where the approve to.
        :param amount: the amount of asset want to approve.
        :param payer: an Account class that used to pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: hexadecimal transaction hash value.
        """
        if sender is None:
            raise SDKException(ErrorCode.param_err('the sender should not be None.'))
        if payer is None:
            raise SDKException(ErrorCode.param_err('the payer should not be None.'))
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('the gas price should be equal or greater than zero.'))
        if gas_limit < 0:
            raise SDKException(ErrorCode.other_error('the gas limit should be equal or greater than zero.'))
        b58_sender_address = sender.get_address_base58()
        b58_payer_address = payer.get_address_base58()
        tx = Asset.new_approve_transaction(asset, b58_sender_address, b58_recv_address, amount, b58_payer_address,
                                           gas_limit, gas_price)
        tx = self.__sdk.sign_transaction(tx, sender)
        if sender.get_address_base58() != payer.get_address_base58():
            tx = self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def send_transfer_from(self, asset: str, sender: Account, b58_from_address: str, b58_recv_address: str, amount: int,
                           payer: Account, gas_limit: int, gas_price: int) -> str:
        """
        This interface is used to generate a Transaction object for transfer that
        allow one account to transfer a amount of ONT or ONG Asset to another account,
        in the condition of the first account had been approved.

        :param asset: a string which is used to indicate which asset we want to transfer.
        :param sender: an Account class that send the transfer transaction.
        :param b58_from_address: a base58 encode address which indicate where the asset from.
        :param b58_recv_address: a base58 encode address which indicate where the asset to.
        :param amount: the amount of asset want to transfer from from-address.
        :param payer: an Account class that used to pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: hexadecimal transaction hash value.
        """
        if sender is None:
            raise SDKException(ErrorCode.param_err('the sender should not be None.'))
        if payer is None:
            raise SDKException(ErrorCode.param_err('the payer should not be None.'))
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('the gas price should be equal or greater than zero.'))
        if gas_limit < 0:
            raise SDKException(ErrorCode.other_error('the gas limit should be equal or greater than zero.'))
        b58_payer_address = payer.get_address_base58()
        b58_sender_address = sender.get_address_base58()
        tx = Asset.new_transfer_from_transaction(asset, b58_sender_address, b58_from_address, b58_recv_address, amount,
                                                 b58_payer_address, gas_limit, gas_price)
        tx = self.__sdk.sign_transaction(tx, sender)
        if b58_sender_address != b58_payer_address:
            tx = self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

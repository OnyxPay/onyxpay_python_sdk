#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from ontology.crypto.digest import Digest
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.contract_data import ContractDataParser


class MerkleVerifier(object):
    @staticmethod
    def get_proof(tx_block_height: int, target_hash_list: List[str], current_block_height: int):
        proof_node = list()
        last_node = current_block_height
        pos = 0
        while last_node > 0:
            if tx_block_height % 2 == 1:
                dict_node = dict(Direction='Left', TargetHash=target_hash_list[pos])
                proof_node.append(dict_node)
                pos += 1
            elif tx_block_height < last_node:
                dict_node = dict(Direction='Right', TargetHash=target_hash_list[pos])
                proof_node.append(dict_node)
                pos += 1
            tx_block_height //= 2
            last_node //= 2
        return proof_node

    @staticmethod
    def validate_proof(proof: List[dict], hex_target_hash: str, hex_merkle_root: str, is_big_endian: bool = False):
        if is_big_endian:
            hex_merkle_root = ContractDataParser.to_reserve_hex_str(hex_merkle_root)
            hex_target_hash = ContractDataParser.to_reserve_hex_str(hex_target_hash)
        if len(proof) == 0:
            return hex_target_hash == hex_merkle_root
        else:
            hex_proof_hash = hex_target_hash
            for node in proof:
                if is_big_endian:
                    sibling = ContractDataParser.to_reserve_hex_str(node['TargetHash'])
                else:
                    sibling = node['TargetHash']
                try:
                    direction = node['Direction'].lower()
                except KeyError:
                    raise SDKException(ErrorCode.other_error('Invalid proof'))
                if direction == 'left':
                    value = bytes.fromhex('01' + sibling + hex_proof_hash)
                    hex_proof_hash = Digest.sha256(value, is_hex=True)
                elif direction == 'right':
                    value = bytes.fromhex('01' + hex_proof_hash + sibling)
                    hex_proof_hash = Digest.sha256(value, is_hex=True)
                else:
                    raise SDKException(ErrorCode.other_error('Invalid proof.'))
            return hex_proof_hash == hex_merkle_root

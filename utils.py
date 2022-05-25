import secrets
import cryptnoxpy
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from tabulate import tabulate
from web3 import Web3
from typing import NewType
import json

HexStr = NewType('HexStr', str)
HexAddress = NewType('HexAddress', HexStr)
ChecksumAddress = NewType('ChecksumAddress', HexAddress)


def _private_key_check(card: cryptnoxpy.Card, public_key: bytes):
        print("Checking private key on the card...")

        nonce = secrets.token_bytes(nbytes=16)
        signature_check = card.signature_check(nonce)
        if signature_check.message[2:18] != nonce:
            print("FAILED!\nPublic and private key differ")
            return "FAILED!\nPublic and private key differ"

        try:
            public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), public_key)
        except ValueError:
            print("FAILED!\nInvalid public key")
            return "FAILED!\nInvalid public key"

        try:
            public_key.verify(signature_check.signature, signature_check.message,
                              ec.ECDSA(hashes.SHA256()))
        except cryptography.exceptions.InvalidSignature:
            print("FAILED!\nPublic and private key differ")
            return "FAILED!\nPublic and private key differ"
        else:
            print("OK")
            return "OK"

def _history_counter(card: cryptnoxpy.Card):
        print("Checking signature counter and history...")
        signature_counter = card.signing_counter
        history = []
        index = 0
        entry = card.history(index)
        while entry.signing_counter != 0:
            history.append([entry.signing_counter, entry.hashed_data.hex()])
            index += 1
            entry = card.history(index)
        ret_message = ''
        print(f"Signature counter: {signature_counter}")
        ret_message+=f"Signature counter: {signature_counter}\n"
        if history:
            ret_message+=tabulate(history)
            return ret_message
        else:
            return "No history entries."

def _owner(endpoint: str, contract_address: ChecksumAddress, abi: str, account: str, nft_id: int) -> None:
        print(f"Checking owner on contract: {contract_address}...")
        print(contract_address)
        w3 = Web3(Web3.HTTPProvider(endpoint))
        try:
            contract = w3.eth.contract(address=contract_address, abi=abi)
        except ValueError as e:
            print(f"ABI format is not json:{e}")
            return f"ABI format is not json:{e}"

        function = contract.get_function_by_name("balanceOf")
        try:
            if function(account, int(nft_id)).call() == 1:
                print("OK")
                return "OK"
            else:
                print(f"FAILED\nThe NFT doesn't belong to address: {account}")
                return f"FAILED\nThe NFT doesn't belong to address: {account}"
        except Exception:
            print("FAILED!\nIssue with checking ownership")
            return "FAILED!\nIssue with checking ownership"


def _balance(endpoint, address):
        try:
            w3 = Web3(Web3.HTTPProvider(endpoint))
            print(f"Balance: {Web3.fromWei(w3.eth.get_balance(address), 'ether')} ETH")
            return f"Balance: {Web3.fromWei(w3.eth.get_balance(address), 'ether')} ETH"
        except Exception as error:
            print(f"Error getting balance: {error}")
            return f"Error getting balance: {error}"

def _url(metadata) -> None:
        try:
            metadata_json = json.loads(metadata)
        except json.decoder.JSONDecodeError:
            print("Error parsing metadata")
            return "Error parsing metadata"
        else:
            try:
                print(metadata_json['image'])
                return metadata_json['image']
            except KeyError:
                try:
                    print(f"https://ipfs.io/ipfs/{metadata_json['image_url'].split('//')[1]}")
                    return f"https://ipfs.io/ipfs/{metadata_json['image_url'].split('//')[1]}"
                except (KeyError, IndexError):
                    print("Can't find image")
                    return "Can't find image"
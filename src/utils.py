import secrets
import cryptnoxpy
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import sha3 as keccak
from tabulate import tabulate
from web3 import Web3
from typing import NewType
import json
import wx
import sha3 as keccak
import hashlib
from ECP256k1 import ECPoint,inverse_mod
from decimal import DefaultContext, Decimal
from pprint import pformat
from sys import version_info
from eth_utils.curried import keccak as eth_keccak
from web3 import Web3

HexStr = NewType('HexStr', str)
HexAddress = NewType('HexAddress', HexStr)
ChecksumAddress = NewType('ChecksumAddress', HexAddress)

USER_SCREEN = (
            "\n>> !!!  Once approved, check on your device screen to confirm the signature  !!! <<"
        )
DECIMALS_FUNCTION = "313ce567"
ETH_DECIMALS = 18
TRANSFERT_FUNCTION = "a9059cbb"
uint_types = [f"uint{type_len}" for type_len in range(8, 257)]
int_types = [f"int{type_len}" for type_len in range(8, 257)]
bytes_types = [f"bytes{type_len}" for type_len in range(1, 33)]
std_types = ["bool", *uint_types, *int_types, "address", *bytes_types, "bytes", "string"]

def address(public_key: str) -> str:
    return eth_keccak(hexstr=("0x" + public_key[2:]))[-20:].hex()


def checksum_address(public_key: str) -> str:
    return Web3.toChecksumAddress(address(public_key))

def get_cryptnox_card():
        index = 0
        card = None
        while index < 5:
            print(f'Getting card index: ({index})')
            try:
                conn = cryptnoxpy.Connection(index)
                card = cryptnoxpy.factory.get_card(conn)
                return card
            except Exception as e:
                print(f'Get card error on index ({index}): {e}')
            index+=1
        return card

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
        print('Got card history')
        while entry.signing_counter != 0:
            print(f'Got signing counter index: {index}')
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
                return f"FAILED - The NFT doesn't belong to address"
        except Exception:
            print("FAILED!\nIssue with checking ownership")
            return "FAILED - Issue with checking ownership"


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

def confirm(parent=None, message=''):
    dlg = wx.MessageDialog(parent,message,caption='Action confirmation', style=wx.OK | wx.CANCEL)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

def format_checksum_address(addr):
    # Format an ETH address with checksum (without 0x)
    addr = addr.lower()
    addr_sha3hash = keccak.keccak_256((addr.encode("ascii"))).digest().hex()
    cs_address = ""
    for idx, ci in enumerate(addr):
        if ci in "abcdef":
            cs_address += ci.upper() if int(addr_sha3hash[idx], 16) >= 8 else ci
            continue
        cs_address += ci
    return cs_address

def compare_eth_addresses(addr1, addr2):
    """Compare 2 ethereum-compatible addresses.
    Accept 0x or hex, lower, upper or mixed "checksummed".
    Does not check for their validity.
    """
    if addr1.startswith("0x"):
        addr1 = addr1[2:]
    if addr2.startswith("0x"):
        addr2 = addr2[2:]
    return addr1.lower() == addr2.lower()

def sha3(raw_message):
    return keccak.keccak_256(raw_message).digest()

def sha2(raw_message):
    """SHA-2 256"""
    return hashlib.sha256(raw_message).digest()

def ask(parent=None, message=''):
    dlg = wx.TextEntryDialog(parent, message)
    action = dlg.ShowModal()
    if action == 5100:
        result = dlg.GetValue()
    elif action == 5101:
        result = None
    else:
        print('Unknown action')
    print(result)
    dlg.Destroy()
    return result

def encode_datasign(datahash, signature_der,pubkey):
        """Encode a message signature from the DER sig."""
        # Signature decoding
        lenr = int(signature_der[3])
        lens = int(signature_der[5 + lenr])
        r = int.from_bytes(signature_der[4 : lenr + 4], "big")
        s = int.from_bytes(signature_der[lenr + 6 : lenr + 6 + lens], "big")
        # Parity recovery
        v = 27
        h = int.from_bytes(datahash, "big")
        if public_key_recover(h, r, s, v) != pubkey:
            v += 1
        # Signature encoding
        return uint256(r) + uint256(s) + bytes([v])

def uint256(i):
    """Integer to 256bits bytes for uint EVM"""
    return i.to_bytes(32, byteorder="big")

def public_key_recover(hash_val, r_sig, s_sig, parity=0):
    CURVES_ORDER = {
    "K1": int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141", 16),
    "R1": int("115792089210356248762697446949407573529996955224135760342422259061068512044369"),
    }
    """Recover public key from hash and signature"""
    curve_order = CURVES_ORDER["K1"]
    # Q = (s.R - h.G) / r
    r_point = ECPoint.from_x(r_sig, parity)
    qpub = inverse_mod(r_sig, curve_order) * r_point.dual_mult(-hash_val % curve_order, s_sig)
    # Uncompressed format 04 X Y
    return qpub.encode_output(False)

def balance_string(amount, decimshift=0):
    utils_decimal_ctx = DefaultContext.copy()
    POINT_CHAR = "."
    ZERO_CHAR = "0"
    """Convert integer shifted by decimshift decimals units
    into a human float string.
    """
    if not isinstance(amount, int):
        raise ValueError("amount arg must be int")
    if decimshift < 0:
        raise ValueError("decimshift must be postive or null")
    num = utils_decimal_ctx.scaleb(Decimal(amount, utils_decimal_ctx), -decimshift)
    if num.is_zero():
        return ZERO_CHAR
    bal_res = f"{num:.{decimshift}f}"
    if len(bal_res) > 1 and POINT_CHAR in bal_res[:-1]:
        bal_res = bal_res.rstrip(ZERO_CHAR)
    if bal_res[-1] == POINT_CHAR:
        bal_res = bal_res[:-1]
    return bal_res

def add_signature(self, signature_der):
        """Add a DER signature into the built transaction."""
        # Signature decoding
        lenr = int(signature_der[3])
        lens = int(signature_der[5 + lenr])
        r = int.from_bytes(signature_der[4 : lenr + 4], "big")
        s = int.from_bytes(signature_der[lenr + 6 : lenr + 6 + lens], "big")
        # Parity recovery
        i = 35
        h = int.from_bytes(self.datahash, "big")
        if public_key_recover(h, r, s, i) != self.pubkey:
            i += 1
        # Signature encoding
        v = int2bytearray(2 * self.chainID + i)
        r = int2bytearray(r)
        s = int2bytearray(s)
        tx_final = rlp_encode(
            [
                self.nonce,
                self.gasprice,
                self.startgas,
                self.to,
                self.value,
                self.data,
                v,
                r,
                s,
            ]
        )
        return tx_final.hex()

def add_vrs(self, vrs):
        # v from Ledger hardware device is only the 8 bits LSB
        v_high = self.chainID >> 7
        v = int2bytearray(256 * v_high + vrs[0])
        r = int2bytearray(vrs[1])
        s = int2bytearray(vrs[2])
        tx_final = rlp_encode(
            [
                self.nonce,
                self.gasprice,
                self.startgas,
                self.to,
                self.value,
                self.data,
                v,
                r,
                s,
            ]
        )
        return tx_final.hex()

def rlp_encode(input_data):
    if isinstance(input_data, int):
        if input_data < 0:
            raise ValueError("RLP encoding error : integer must be positive or null")
        return rlp_encode(to_binary(input_data))
    if isinstance(input_data, bytearray):
        if len(input_data) == 1 and input_data[0] == 0:
            return bytearray(b"\x80")
        if len(input_data) == 1 and input_data[0] < 0x80:
            return input_data
        return encode_length(len(input_data), 0x80) + input_data
    if isinstance(input_data, list):
        output = bytearray([])
        for item in input_data:
            output += rlp_encode(item)
        return encode_length(len(output), 0xC0) + output
    raise ValueError("Bad input_data type : int, list or bytearray required")

def encode_length(Lon, offset):
    if Lon < 56:
        return bytearray([Lon + offset])
    BLon = to_binary(Lon)
    return bytearray([len(BLon) + offset + 55]) + BLon

def to_binary(x):
    if x == 0:
        return bytearray([])
    return to_binary(int(x // 256)) + bytearray([x % 256])

def int2bytearray(i):
    barr = (i).to_bytes(32, byteorder="big")
    while barr[0] == 0 and len(barr) > 1:
        barr = barr[1:]
    return bytearray(barr)

def shift_10(num_str, shift):
    utils_decimal_ctx = DefaultContext.copy()
    """Multiply by power of 10 at the string level, args >= 0"""
    # Act like a point shifter
    # Avoid floating point issues
    if not isinstance(num_str, str):
        raise ValueError("num_str must be string")
    if not isinstance(shift, int):
        raise ValueError("shift must be integer")
    if shift < 0:
        raise ValueError("shift must be postive or null")
    return int(utils_decimal_ctx.scaleb(Decimal(num_str, utils_decimal_ctx), shift))

def print_text_query(query_obj):
    """Generate the string for user display approval."""
    format_args = {"indent": 4}
    if version_info >= (3, 8):
        format_args["sort_dicts"] = False
    datam = pformat(query_obj["message"], **format_args)
    return f"{query_obj['primaryType']}\n{datam}\n"

def encode_value(vtype, value, go):
    """Encode a given value in Python bytes."""
    if vtype == "bool":
        if not isinstance(value, bool):
            raise ValueError("bool type is not a bool value.")
        return uint256(1) if value else uint256(0)
    if vtype == "address":
        if not isinstance(value, str):
            raise ValueError("address type is not a str value.")
        if len(value) != 42 or value[:2] != "0x":
            raise ValueError("address is not a 0x hex value.")
        try:
            int_value = int(value[2:], 16)
        except ValueError:
            raise ValueError("address is not a 0x hex value.")
        return uint256(int_value)
    if vtype in int_types or vtype in uint_types:
        if isinstance(value, str):
            # Fallback for dapp encoding uint as string
            try:
                value = int(value, 10)
            except ValueError:
                raise ValueError(vtype + " is not a valid string.")
        if not isinstance(value, int):
            raise ValueError(vtype + " type is not a int nor str value.")
        if value >= 0:
            intval_bin = uint256(value)
        else:
            intval_bin = uint256(2 ** 256 + value)
        return intval_bin
    if vtype in bytes_types:
        if not isinstance(value, str):
            raise ValueError("bytes type is not a str value.")
        if value[:2] != "0x":
            raise ValueError("bytes is not a 0x hex value.")
        try:
            out = bytes.fromhex(value[2:])
        except ValueError:
            raise ValueError("bytes is not a 0x hex value.")
        while len(out) < 32:
            out += b"\0"
        return out
    if vtype == "bytes":
        if not isinstance(value, str):
            raise ValueError("bytes type is not a str value.")
        if value[:2] != "0x":
            raise ValueError("bytes is not a 0x hex value.")
        try:
            out = bytes.fromhex(value[2:])
        except ValueError:
            raise ValueError("bytes is not a 0x hex value.")
        return sha3(out)
    if vtype == "string":
        if not isinstance(value, str):
            raise ValueError("string type is not a str value.")
        return sha3(value.encode("utf8"))
    if vtype.endswith("[]"):
        if not isinstance(value, list):
            raise ValueError("array type is not a list value.")
        elements = [encode_value(vtype[:-2], val, go) for val in value]
        return sha3(b"".join(elements))
    # Should be a struct finally
    if not isinstance(value, dict):
        raise ValueError("struct type is not a dict value.")
    return hash_struct(vtype, go, value)

def encode_atype(name, types_list):
    """Encode a struct type string for typeHash."""
    member_list = []
    for member in types_list:
        if "name" in member:
            member_list.append(f"{member['type']} {member['name']}")
    return f"{name}({','.join(member_list)})"

def encode_types(types_list, types_dict):
    """Provide the struct type string signature (encodeType)."""
    types_enc = ""
    for type_key in types_list:
        if type_key.endswith("[]"):
            type_key = type_key[:-2]
        types_enc += encode_atype(type_key, types_dict[type_key])
    return types_enc

def collect_sub_types(name, types_obj, list_types=None):
    """Collect all types of a struct."""
    if not list_types:
        list_types = []
    if name.endswith("[]"):
        name = name[:-2]
    if name in list_types:
        return list_types
    if name not in types_obj.keys():
        return list_types
    list_types.append(name)
    for member in types_obj[name]:
        for submember in collect_sub_types(member["type"], types_obj, list_types):
            if submember in std_types:
                continue
            if submember not in list_types:
                list_types.append(submember)
    return list_types[1:]

def type_hash(name, types_obj):
    """Compute typeHash (hash of the encodeType type string)."""
    subtypes_list = collect_sub_types(name, types_obj)
    subtypes_list.sort()
    types_list = [name, *subtypes_list]
    return sha3(encode_types(types_list, types_obj).encode("utf8"))

def hash_struct(name, types_obj, data_obj):
    """Compute the hashStruct = keccak256(typeHash ‖ encodeData(s))."""
    return sha3(type_hash(name, types_obj) + encode_data(name, types_obj, data_obj))

def encode_data(name, types_obj, data_obj):
    """encodeData : Encode all the data of the members values."""
    out = b""
    for member in types_obj[name]:
        if "name" in member:
            mvalue = data_obj[member["name"]]
            mtype = member["type"]
            if isinstance(mvalue, dict):
                out += hash_struct(mtype, types_obj, mvalue)
            else:
                out += encode_value(mtype, mvalue, types_obj)
    return out

def typed_sign_hash(query_obj, chain_id=None):
    """Compute the hash to sign form the typed data object."""

    # Checking the query format
    if "primaryType" not in query_obj:
        raise ValueError("Missing primaryType in typedhash query.")
    if "types" not in query_obj:
        raise ValueError("Missing types in typedhash query.")
    if "EIP712Domain" not in query_obj["types"]:
        raise ValueError("Missing EIP712Domain in typedhash.types.")
    if query_obj["primaryType"] not in query_obj["types"]:
        if query_obj["primaryType"] not in std_types:
            raise ValueError("Missing primary type in typedhash.types query.")
    if "message" not in query_obj:
        raise ValueError("Missing message in typedhash query.")
    if "domain" not in query_obj:
        raise ValueError("Missing domain in typedhash query.")
    if chain_id is not None and "chainId" in query_obj["domain"]:
        if chain_id != query_obj["domain"]["chainId"]:
            raise ValueError("ChainID is not matching the current active chain.")

    domain_separator = hash_struct("EIP712Domain", query_obj["types"], query_obj["domain"])
    hash_msg = hash_struct(query_obj["primaryType"], query_obj["types"], query_obj["message"])

    return domain_separator, hash_msg


#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction

#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance
#Private key: Jo1VzgASXoDFfcP9mGk6aeZqnQioAb/BgS3YNGhjPbc8UEgOTLER2NYU7SLz8Kh8N0F211kzZdX3G9ipk13bZg==
#Address: HRIEQDSMWEI5RVQU5URPH4FIPQ3UC5WXLEZWLVPXDPMKTE253NTOZLVVUI

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here

    sender_private_key = 'Jo1VzgASXoDFfcP9mGk6aeZqnQioAb/BgS3YNGhjPbc8UEgOTLER2NYU7SLz8Kh8N0F211kzZdX3G9ipk13bZg=='
    sender_address = 'HRIEQDSMWEI5RVQU5URPH4FIPQ3UC5WXLEZWLVPXDPMKTE253NTOZLVVUI'
    recipient_address = receiver_pk
    payment_txn = transaction.PaymentTxn(
        sender=sender_address,
        fee = tx_fee ,
        first = first_valid_round,
        last = last_valid_round,
        gh = gen_hash,
        receiver=recipient_address,
        amt=tx_amount,  # Amount in microalgos (1 ALGO = 1,000,000 microalgos)
    )
    # Sign the transaction with the sender's private key
    signed_txn = payment_txn.sign(sender_private_key)

    # Send the signed transaction to the blockchain
    txid = algod_client.send_transaction(signed_txn)
    return sender_address , txid


# Function from Algorand Inc.

def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo


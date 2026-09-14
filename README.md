# SecureMessage - Single Token Flask Website

## What changed

This version does NOT give the user a separate encrypted message and encryption key.

It creates ONE token:

SM1.xxxxxxxxxxxxxxxxxxxxx

The token contains:
- AES-256 encryption key
- nonce
- encrypted ciphertext
- token metadata

The receiver only pastes this one token into the Decrypt page.

## Install

pip install -r requirements.txt

## Run

python app.py

Then open:

http://127.0.0.1:5000

## Security

AES-256-GCM provides authenticated encryption, so modified tokens fail decryption.

IMPORTANT:
The token contains everything required for decryption. Anyone who gets the token can decrypt the message.

For production:
- use HTTPS
- set debug=False
- do not log tokens or plaintext
- add rate limiting
- use secure headers

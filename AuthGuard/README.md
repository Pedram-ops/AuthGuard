# AuthGuard

AuthGuard is an open-source two-factor authentication software that allows users to generate one-time passwords (OTP) for their accounts. This software functions similarly to Google Authenticator and utilizes the TOTP (Time-based One-Time Password) algorithm.

## Features

- User registration with code name and secret key
- Automatic generation of one-time passwords (OTP)
- QR Code generation for easier registration
- User information stored in an SQLite database
- Simple and user-friendly interface

## Prerequisites

Before running the program, ensure that the following libraries are installed:

- `pyotp`
- `qrcode`
- `tkinter`
- `sqlite3`

You can install these libraries using pip:

```bash
pip install pyotp qrcode[pil]


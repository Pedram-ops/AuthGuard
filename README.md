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

'''
# How to Use
1- Run the software. 
2- In the "Code Name" field, enter your code name.
3- In the "Your Key" field, enter your secret key.
4- Click the "Register" button.
5- The generated QR Code can be scanned or the key can be entered into your authentication app.
6- One-time passwords (OTP) for your account will be generated automatically.

# Contributing
If you would like to contribute to the development of this project, please follow these steps:

1- Fork this repository.
2- Make your changes.
3- Submit a Pull Request.

# License
This project is licensed under the MIT License. Please see the LICENSE file for more details.

# Contact
For any questions or suggestions, feel free to reach out to me:

Email: bahloolip@gmail.com
GitHub: Pedram-Ops

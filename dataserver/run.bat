:: alright this batch file, when run, will create a .venv if it doest exist,
::use .venv
::upgrade pip and packages
::doesnt currently handle upgrading the packages or anything
::
::Written by a probably dumb Matt Wockenfuss 9-21-2025
@echo off


IF NOT EXIST ".venv\" (
    echo ".venv DOESNT EXIST, CREATING"
    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install websockets
    pip install pyyaml
    pip install pillow
    python server.py
    pause
) ELSE (
    .venv\Scripts\activate
    echo ".venv ALREADY EXISTS"
    python server.py
    pause
)

:: run.bat
::
:: This batch file automates the setup and running of the Python MMO server environment.
:: When executed, it:
:: - Checks if a virtual environment folder ".venv" exists.
:: - If not present, it creates the virtual environment, activates it,
::   upgrades pip, installs required Python packages, then runs server.py.
:: - If the environment already exists, it activates it and runs server.py directly.
:: - After running the server, it pauses so output can be reviewed.
:: - Finally, it prompts to restart the script (though this is not handled automatically).
::
:: Written by Matt Wockenfuss on 9-21-2025.
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



echo "Would you like to restart? (Y/N)"
pause
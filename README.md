# NII LOR Speech recognition
This is a student project of NII LOR and Peter the Great St.Petersburg Polytechnic University (SPbPU) that helps a patient to test their ear.
More information can be found at docs: `docs/Руководство Пользователя.docx`

## Project goal
TBD 

## Getting started

## Pre-requisites
- Windows 10 (x64)
- Internet connection
- 1Gb free space on hard drive

## Technology stack
- [Python 3.x](https://www.python.org/)
- Batch scripts

## The First run
In order to start working with project just launch `bin\startup.bat`.
The script then perform following actions:
- clean `workdir`and create them if not exist;
- install required software from `soft` folder;
- launches desktop application.

## The Second run
If the software (Python and its packages) is already installed, then user may use only:
- launch `query_application.bat` script from 'bin' directory' in order to bring up the application.
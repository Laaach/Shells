# Shells
Script that automates generating reverse shells for different languages using msfvenom. Saves LHOST and LPORT locally so you don't have to type them every time.
## Usage
Install dependencies first:
```bash
pip install -r requirements.txt
```
Then run:
```bash
python3 shells.py
```
Use `-r` or `--reset` to overwrite saved LHOST/LPORT.
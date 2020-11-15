import re
import json
import importlib
from threading import Thread, Event
from pathlib import Path

from labylib import Cape

name = "animated-textures"

class Config:
	
	textures = f"./{name}/" # Cosmetic textures path
	f = f"./{name}/config.json" # JSON Config file
	default = '{"PHPSESSID": "","cosmetics": {"cape": {"interval": "15","randomOrder": "False"}}}' # Default config
	pattern = "^[-,a-zA-Z0-9]{1,128}$" # PHPSESSID pattern

	def __init__(self):
		self.config = None
		self.exists = True # Config file already exists
		self.load()

	# Example: getCosmetic("cape")
	def getCosmetic(self,key):
		return self.config["cosmetics"][key]

	# Example: setCosmetic("cape","interval",30)
	def setCosmetic(self,cosmetic,key,value):
		self.config["cosmetics"][cosmetic][key] = value
		self.save()

	def setPHPSESSID(self,phpsessid):
		self.config["PHPSESSID"] = phpsessid
		self.save()

	# -----------------------------------------------------

	# (Over)write config file
	def save(self):
		f = open(Config.f,"w")
		f.write(json.dumps(self.config))
		f.close()

	# Create config file from default template
	def create(self):
		self.exists = False

		Path(Config.textures).mkdir(parents=True,exist_ok=True)

		f = open(Config.f,"w")
		f.write(Config.default)
		f.close()

	# Load the config file from disk into memory
	def load(self):
		# Create config file if absent
		if(Path(Config.f).is_file() == False):
			self.create()

		f = open(Config.f,"r")
		self.config = json.load(f)
		f.close()

		return True

class Labylib(Thread):

	clock = 1

	def __init__(self,event,phpsessid,cosmetic):
		Thread.__init__(self)
		self.stopped = event
		self.phpsessid = phpsessid

		self.cosmetic = cosmetic.capitalize()
		self.textures = self.scandir()
		self.index = 0

		self.interval = 0
		self.cooldown = 15

	def scandir(self):
		files = Path("./animated-textures/cape/").glob("**/*")
		return [x for x in files if x.is_file()]

	def updateCosmetic(self):
		# Reset index if last texture in dir
		if(self.index > len(self.textures) - 1):
			self.index = 0

		texture = self.textures[self.index]

		labylib = globals()[self.cosmetic].Texture(self.phpsessid,texture)
		labylib.update()

		self.index = self.index + 1

	def run(self):
		while not self.stopped.wait(Labylib.clock):
			if(self.interval >= self.cooldown):
				self.updateCosmetic()
				self.interval = 0
			self.interval = self.interval + 1

class Main:
	
	def __init__(self):
		self.config = Config()
		self.init()

	# Guided step-by-step setup
	def wizard(self):
		# +-----------+
		# |  Labylib  |
		# +-----------+
		def box(string):
			charset = ["+","-","|"] # Corner,borderX,borderY
			string = f"  {string}  " # Text padding

			box = charset[0]
			# Repeat 'borderX' char for string length
			for x in string:
				box += charset[1]
			box += charset[0]

			# Stitch it all together
			string = f"{charset[2]}{string}{charset[2]}"
			string = f"{box}\n{string}\n{box}"

			return string

		msgDone = "Done! Closing Wizard"

		print(box("Labylib Setup Wizard"))
		print("Make sure you read the README before you begin:")
		print("https://github.com/VictorWesterlund/labylib/blob/master/README.md\n")

		self.config.setPHPSESSID(input("Paste your PHPSESSID here:\n"))

		advanced = input("\nDo you wish to modify the default cosmetic settings? 'y/n'[n]: ")
		if(advanced != "y"):
			print(box(msgDone))
			self.start()
			return
		
		wizard = self.config.config["cosmetics"]

		# Iterate over all cosmetics in config
		for cosmetic in wizard:
			print(box("Cosmetic > " + cosmetic.capitalize()))

			# Iterate over every cosmetic setting
			for key, default in wizard[cosmetic].items():
				value = input(f"Set value for '{key}'[{default}]: ")
				# Ignore input if empty or data type doesn't match default
				if(len(value) < 1):
					print(f"Input error: Expected data type '{type(default)}'. Falling back to default")
					value = default

				self.config.setCosmetic(cosmetic,key,value)
		
		print(box(msgDone))
		self.start()

	def start(self):
		phpsessid = self.config.config["PHPSESSID"]
		start = input(f"\nStart Labylib for PHPSESSID '{phpsessid}'? 'y/n/config'[y]: ")

		if(start == "n"):
			return

		if(start == "config"):
			self.wizard()
			return

		stop = Event()
		for cosmetic in self.config.config["cosmetics"]:
			thread = Labylib(stop,self.config.config["PHPSESSID"],cosmetic)
			thread.start()

		interrupt = input("Running! Press enter to stop\n")
		stop.set()
		print("Bye!")

	def init(self):
		print("THIS PROGRAM IS STILL IN PRE-RELEASE. EXPECT QUIRKINESS\n")
		if(self.config.exists and len(self.config.config["PHPSESSID"]) > 1):
			self.start()
			return

		for cosmetic in self.config.config["cosmetics"]:
			Path(Config.textures + cosmetic).mkdir(parents=True,exist_ok=True)

		# Prompt if user wants to use guided setup
		print("-- Labylib Animated Textures --\nSince this is your first time here, would you like to walk through the setup process?\n")
		wizard = input("Start guided setup? 'y/n':[y] ")
		if(wizard == "n"):
			print(f"A config file '{Config.f}' has been created for you. Run this command again when you're ready")
			return

		self.wizard()
		
# Start Labylib
labylib = Main()
from Position import Position
from Organisms.Plant import Plant
from Action import Action
from ActionEnum import ActionEnum
from Organisms.Grass import Grass
from Organisms.Antylopa import Antylopa
from Organisms.Rys import Rys
from Organisms.Sheep import Sheep
import random

class World(object):

	def __init__(self, worldX, worldY):
		self.__worldX = worldX
		self.__worldY = worldY
		self.__turn = 0
		self.__organisms = []
		self.__newOrganisms = []
		self.__separator = '.'
		#inicjalizacja wartosci plagi
		self.__plague_mode = False
		self.__plague_turns_left = 2

	@property
	def worldX(self):
		return self.__worldX

	@property
	def worldY(self):
		return self.__worldY

	@property
	def turn(self):
		return self.__turn

	@turn.setter
	def turn(self, value):
		self.__turn = value

	@property
	def organisms(self):
		return self.__organisms

	@organisms.setter
	def organisms(self, value):
		self.__organisms = value

	@property
	def newOrganisms(self):
		return self.__newOrganisms

	@newOrganisms.setter
	def newOrganisms(self, value):
		self.__newOrganisms = value

	@property
	def separator(self):
		return self.__separator

	def makeTurn(self):
		actions = []

		#sprawdzenie czy plaga aktyna i zmiana wartosci
		if self.__plague_mode:
			self.__plague_turns_left -= 1
			print('Plague mode active! Turns left: ' + str(self.__plague_turns_left))
			if self.__plague_turns_left == 0:
				self.__plague_mode = False
				print('Plague mode deactivated!')

		for org in self.organisms:
			if self.positionOnBoard(org.position):
				actions = org.move()
				for a in actions:
					self.makeMove(a)
				actions = []
				if self.positionOnBoard(org.position):
					actions = org.action()
					for a in actions:
						self.makeMove(a)
					actions = []

		self.organisms = [o for o in self.organisms if self.positionOnBoard(o.position)]
		for o in self.organisms:
			o.liveLength -= 1
			if self.__plague_mode:
				o.liveLength //= 2 # Skracanie życia o połowę
			o.power += 1
			if o.liveLength < 1:
				print(str(o.__class__.__name__) + ': died of old age at: ' + str(o.position))
		self.organisms = [o for o in self.organisms if o.liveLength > 0]

		self.newOrganisms = [o for o in self.newOrganisms if self.positionOnBoard(o.position)]
		self.organisms.extend(self.newOrganisms)
		self.organisms.sort(key=lambda o: o.initiative, reverse=True)
		self.newOrganisms = []

		self.Extinct()
		self.turn += 1
		
	
	def Extinct(self):
		organism_types = [Grass, Antylopa, Rys, Sheep]
		

		for organism_type in organism_types:
			if not any(isinstance(o, organism_type) for o in self.organisms):
				print(f'Organizm {organism_type.__name__} zostanie przywrocony na losowa pozycje!')
			
			# Tworzenie nowego organizmu tego samego typu na losowej pozycji
			while True:
				new_position = Position(xPosition=random.randint(0, self.worldX - 1),
                                        yPosition=random.randint(0, self.worldY - 1))
				if self.getOrganismFromPosition(new_position) is None:
					break
				
				
			new_organism = organism_type(position=new_position, world=self)
			new_organism.initParams()
			self.addOrganism(new_organism)

	def makeMove(self, action):
		print(action)
		if action.action == ActionEnum.A_ADD:
			self.newOrganisms.append(action.organism)
		elif action.action == ActionEnum.A_INCREASEPOWER:
			action.organism.power += action.value
		elif action.action == ActionEnum.A_MOVE:
			action.organism.position = action.position
		elif action.action == ActionEnum.A_REMOVE:
			action.organism.position = Position(xPosition=-1, yPosition=-1)

	def addOrganism(self, newOrganism):
		newOrgPosition = Position(xPosition=newOrganism.position.x, yPosition=newOrganism.position.y)

		if self.positionOnBoard(newOrgPosition):
			self.organisms.append(newOrganism)
			self.organisms.sort(key=lambda org: org.initiative, reverse=True)
			return True
		return False

	def positionOnBoard(self, position):
		return position.x >= 0 and position.y >= 0 and position.x < self.worldX and position.y < self.worldY

	def getOrganismFromPosition(self, position):
		pomOrganism = None

		for org in self.organisms:
			if org.position == position:
				pomOrganism = org
				break
		if pomOrganism is None:
			for org in self.newOrganisms:
				if org.position == position:
					pomOrganism = org
					break
		return pomOrganism

	def getNeighboringPositions(self, position):
		result = []
		pomPosition = None

		for y in range(-1, 2):
			for x in range(-1, 2):
				pomPosition = Position(xPosition=position.x + x, yPosition=position.y + y)
				if self.positionOnBoard(pomPosition) and not (y == 0 and x == 0):
					result.append(pomPosition)
		return result

	def filterFreePositions(self, fields):
		result = []

		for field in fields:
			if self.getOrganismFromPosition(field) is None:
				result.append(field)
		return result

	def filterPositionsWithoutAnimals(self, fields):
		result = []
		pomOrg = None

		for filed in fields:
			pomOrg = self.getOrganismFromPosition(filed)
			if pomOrg is None or isinstance(pomOrg, Plant):
				result.append(filed)
		return result

	#PLAGA
	def startPlagueMode(self):
		self.__plague_mode = True
		self.__plague_turns_left = 2

	def __str__(self):
		result = '\nturn: ' + str(self.__turn) + '\n'
		for wY in range(0, self.worldY):
			for wX in range(0, self.worldX):
				org = self.getOrganismFromPosition(Position(xPosition=wX, yPosition=wY))
				if org:
					result += str(org.sign)
				else:
					result += self.separator
			result += '\n'
		return result

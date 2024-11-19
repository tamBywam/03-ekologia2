from .Animal import Animal
from .Rys import Rys
from Action import Action
from ActionEnum import ActionEnum
from Position import Position
import random

class Antylopa(Animal):

	def __init__(self, antylopa=None, position=None, world=None):
		super(Antylopa, self).__init__(antylopa, position, world)

	def clone(self):
		return Antylopa(self, None, None)

	def initParams(self):
		self.power = 4
		self.initiative = 3
		self.liveLength = 11
		self.powerToReproduce = 5
		self.sign = 'A'

	def getNeighboringPosition(self):
		return self.world.filterPositionsWithoutAnimals(self.world.getNeighboringPositions(self.position))
		
	def action(self):
		result = []
		
		
		if self.ifReproduce():
			birthPositions = self.getNeighboringBirthPosition()
			if birthPositions:
				newAnimalPosition = random.choice(birthPositions)
				newAnimal = self.clone()
				newAnimal.initParams()
				newAnimal.position = newAnimalPosition
				self.power = self.power / 2
				result.append(Action(ActionEnum.A_ADD, newAnimalPosition, 0, newAnimal))

		# Sprawdzanie czy obok jest Rys
		rys_nearby = False
		rys_position = None
		neighboring_positions = self.world.getNeighboringPositions(self.position)
		for pos in neighboring_positions:
			if isinstance(self.world.getOrganismFromPosition(pos), Rys):
				rys_nearby = True
				rys_position = pos
				break
			
		# Ucieczka przed Rysiem w kierunku przeciwnym
		if rys_nearby:
			opposite_position_x = self.position.x - (rys_position.x - self.position.x)
			opposite_position_y = self.position.y - (rys_position.y - self.position.y)
			opposite_position = Position(xPosition=opposite_position_x, yPosition=opposite_position_y)
			if self.world.positionOnBoard(opposite_position):
				result.append(Action(ActionEnum.A_MOVE, opposite_position, 0, self))
				print('Antylopa ucieka na pozycje: ', opposite_position)
				
		return result

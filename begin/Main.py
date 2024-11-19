from World import World
from Position import Position
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Organisms.Rys import Rys
from Organisms.Antylopa import Antylopa
from Tests import TestWorld
import unittest
import os


if __name__ == '__main__':
	unittest.main(exit=False)
	pyWorld = World(10, 10)

	newOrg = Grass(position=Position(xPosition=9, yPosition=9), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Grass(position=Position(xPosition=1, yPosition=1), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Sheep(position=Position(xPosition=2, yPosition=2), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Rys(position=Position(xPosition=4, yPosition=5), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Antylopa(position=Position(xPosition=7, yPosition=3), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	print(pyWorld)
	print('"P" plaga\n"N" dodaj organizm')

	for _ in range(0, 50):
		a = input('')
		#wywolanie funkcji rozpoczecia plagi
		if a == 'P':
			pyWorld.startPlagueMode()
		#dodanie organizmu na pozycji
		elif a == 'N':
			newOrg = input('1. Grass\n2. Sheep\n3. Rys\n4. Antylopa\n')
			if newOrg == '1':
				x = int(input('Podaj pozycje x(0-9): '))
				y = int(input('Podaj pozycje y(0-9): '))
				newOrg = Grass(position=Position(xPosition=x, yPosition=y), world=pyWorld)
				pyWorld.addOrganism(newOrg)
			elif newOrg == '2':
				x = int(input('Podaj pozycje x(0-9): '))
				y = int(input('Podaj pozycje y(0-9): '))
				newOrg = Sheep(position=Position(xPosition=x, yPosition=y), world=pyWorld)
				pyWorld.addOrganism(newOrg)
			elif newOrg == '3':
				x = int(input('Podaj pozycje x(0-9): '))
				y = int(input('Podaj pozycje y(0-9): '))
				newOrg = Rys(position=Position(xPosition=x, yPosition=y), world=pyWorld)
				pyWorld.addOrganism(newOrg)
			elif newOrg == '4':
				x = int(input('Podaj pozycje x(0-9): '))
				y = int(input('Podaj pozycje y(0-9): '))
				newOrg = Antylopa(position=Position(xPosition=x, yPosition=y), world=pyWorld)
				pyWorld.addOrganism(newOrg)
		os.system('cls')
		pyWorld.makeTurn()
		print(pyWorld)

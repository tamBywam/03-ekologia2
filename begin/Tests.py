from unittest import TestCase
from World import World
from Position import Position
from Organisms.Antylopa import Antylopa
from Organisms.Rys import Rys
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep

class TestWorld(TestCase):
    def setUp(self):
        # Inicjalizacja świata przed każdym testem
        self.world = World(5, 5)

    def test_plague_mode(self):
        # Testowanie trybu plagi
        self.world.startPlagueMode()
        # Sprawdzenie czy tryb plagi jest aktywny
        self.assertTrue(self.world._World__plague_mode)
        # Sprawdzenie czy liczba pozostałych tur trybu plagi jest prawidłowa
        self.assertEqual(self.world._World__plague_turns_left, 2)

    def test_antylopa_behavior(self):
        # Testowanie zachowania antylopy
        # Tworzenie antylopy i rysia na planszy
        antylopa = Antylopa(position=Position(xPosition=2, yPosition=2), world=self.world)
        rys = Rys(position=Position(xPosition=2, yPosition=3), world=self.world)
        self.world.addOrganism(antylopa)
        self.world.addOrganism(rys)
        # Wywołanie funkcji przetwarzającej turę w świecie
        self.world.makeTurn()
        # Sprawdzenie czy antylopa zmieniła pozycję
        self.assertTrue(antylopa.position != Position(xPosition=2, yPosition=2))

    def test_rys(self):
        # Testowanie tworzenia rysia
        rys = Rys(position=Position(xPosition=2, yPosition=2), world=self.world)
        self.assertIsNotNone(rys)
        self.assertEqual(rys.position, Position(xPosition=2, yPosition=2))

    def test_extinct(self):
        # Testowanie dodawania organizmów, które nie istnieją na planszy
        self.world.organisms = [Grass(position=Position(xPosition=0, yPosition=0), world=self.world),
                                 Antylopa(position=Position(xPosition=1, yPosition=1), world=self.world),
                                 Rys(position=Position(xPosition=2, yPosition=2), world=self.world)]
        # Wywołanie funkcji przetwarzającej turę w świecie
        self.world.makeTurn()
        # Sprawdzenie czy nowe organizmy zostały dodane na planszę
        self.assertTrue(any(isinstance(organism, Sheep) for organism in self.world.organisms))
        self.assertTrue(any(isinstance(organism, Grass) for organism in self.world.organisms))
        self.assertTrue(any(isinstance(organism, Rys) for organism in self.world.organisms))
        self.assertTrue(any(isinstance(organism, Antylopa) for organism in self.world.organisms))

# Vozar Richard
# WFZ4WR
# h053763

from enum import Enum, unique
from random import shuffle, randint
from abc import ABC, abstractmethod


@unique
class Szin(Enum):
	PIKK = 1
	KOR = 2
	KARO = 3
	TREFF = 4


@unique
class Ertek(Enum):
	KETTO = 2
	HAROM = 3
	NEGY = 4
	OT = 5
	HAT = 6
	HET = 7
	NYOLC = 8
	KILENC = 9
	TIZ = 10
	JUMBO = 11
	OLGA = 12
	KIRALY = 13
	ASZ = 14


class Kartya:
	def __init__(self, szin, ertek):
		self._szin = szin
		self._ertek = ertek

	@property
	def szin(self):
		return self._szin
	
	@szin.setter
	def szin(self, ertek):
		if isinstance(ertek, Szin):
			self._szin = szin
		else:
			self._szin = Szin['PIKK']

	@property
	def ertek(self):
		return self._ertek
	
	@ertek.setter
	def ertek(self, ertek):
		if isinstance(ertek, Ertek):
			self._ertek = ertek
		else:
			self._ertek = Ertek(EGY)

	def __str__(self):
		return f'{self._szin.name} {self._ertek.name}'




class Pakli:
	def __init__(self):
		self.pakli = []

		for sz in (Szin):
			for e in (Ertek):
				self.pakli.append(Kartya(sz, e))

	def __str__(self):
		"""
		ret = ''
		i = 1
		for kartya in self.pakli:
			ret += f'{i}: {kartya.szin.name} {kartya.ertek.name}\n'
			i += 1
		return ret
		"""
		return str(len(self.pakli))


	def keveres(self):
		if len(self.pakli) != 52:
			raise ValueError('Megkezdett pakli nem keverhető')
		shuffle(self.pakli)
		return self


	def huzas(self):
		if not len(self.pakli):
			raise ValueError('Ures paklibol nem lehet huzni')
		return self.pakli.pop(randint(0, len(self.pakli)-1))



class Jatekos(ABC):
	def __init__(self, nev):
		self.nev = nev
		self.kartyak = []
		self.gyozelmek = 0


	@abstractmethod
	def huz_vagy_megall(self):
		pass



class Felhasznalo(Jatekos):
	def __init__(self, nev):
		super().__init__(nev)


	"""
	return:
	    -1: kilepes a jatekbol
	    0: megall nem ker tobb lapot
	    1: lapot ker (huz)
	"""
	def huz_vagy_megall(self):
		valasz = input('Lapot huzol / megallsz / kilepes (h/m/q): ').lower()
		if valasz == 'q':
			return -1
		elif valasz == 'h':
			return 1
		elif valasz == 'm':
			return 0
		else:
			print('Rossz input!\nEzek kozul valassz: h/m/q : ')
			self.huz_vagy_megall()



class Bot(Jatekos):
	def __init__(self):
		super().__init__('BlackJack Bot')

	def huz_vagy_megall(self, bot_pont):
		if bot_pont < 14:
			return 1
		else:
			return 0



class BlackJack:
	def __init__(self, nev):
		self.jatek_pakli = Pakli()
		self.felhasznalo = Felhasznalo(nev)
		self.bot = Bot()
		self.kor = 0

		# udvozles
		print('Udv a BlackJack jatekban!\n')
		self.jatek_pakli.keveres()
		print('-- Pakli megkeverve')
		self.start_game()


	def start_game(self):
		# uj kor inicializalasa
		self.jatek_pakli = Pakli()
		self.jatek_pakli.keveres()
		self.kor += 1
		self.felhasznalo.kartyak = []
		self.bot.kartyak = []

		if self.felhasznalo.gyozelmek == 5 or self.bot.gyozelmek == 5:
			self.jatek_vege()

		print(f'\n---------- Lassuk a(z) {self.kor}. kort! ----------')
		print('-- Kezdodjon a jatek!\n')

		print('--Lapok kiosztasa:')
		self.felhasznalo.kartyak.append(self.jatek_pakli.huzas()) # felhasznalo 1. lap
		self.felhasznalo.kartyak.append(self.jatek_pakli.huzas()) # felhasznalo 2. lap
		self.bot.kartyak.append(self.jatek_pakli.huzas()) # bot 1. lap
		self.bot.kartyak.append(self.jatek_pakli.huzas()) # bot 2. lap

		dontes = 1
		# jatekos lepesei az adott korben
		while dontes:

			jatekos_pontjai = self.pontok(self.felhasznalo.kartyak)

			# jatekos lapjainak kiiratasa
			print('--- lapjaid ---')
			i = 1
			for kartya in self.felhasznalo.kartyak:
				print(f'{i}. {kartya}')
				i += 1
			print(f'Pontok: {jatekos_pontjai}')
			print('---------------\n')

			if jatekos_pontjai > 21:
				self.jatekos_vesztett_egy_kort()
			elif jatekos_pontjai == 21:
				print('--- Gratulalok! BLACK JACK! ---\n\n')
				self.jatekos_nyert_egy_kort()
			else:
				dontes = self.felhasznalo.huz_vagy_megall()
				if dontes == 1:
					self.felhasznalo.kartyak.append(self.jatek_pakli.huzas())
					print(f'\n-- Felhuztal egy {self.felhasznalo.kartyak[-1]} lapot')
				elif dontes == 0:
					print(f'-- Megalltal {jatekos_pontjai} ponttal')
				elif dontes == -1:
					print('-- Jatekbol kilepes...')
					self.jatek_vege()
				else:
					print('Na ide baromira nem kellene eljutni soha...')

		# bot lepesei az adott korben
		bot_dontes = 1
		while bot_dontes:
			bot_dontes = self.bot.huz_vagy_megall(self.pontok(self.bot.kartyak))
			if bot_dontes:
				self.bot.kartyak.append(self.jatek_pakli.huzas())

		jatekos_pontjai = self.pontok(self.felhasznalo.kartyak)
		bot_pontjai = self.pontok(self.bot.kartyak)

		print(f'Bot pontjai: {self.pontok(self.bot.kartyak)}')

		if bot_pontjai > 21:
			self.jatekos_nyert_egy_kort()
		else:
			if bot_pontjai == jatekos_pontjai:
				self.jatekos_nyert_egy_kort() if len(self.felhasznalo.kartyak) <= len(self.bot.kartyak) else self.jatekos_vesztett_egy_kort()
			else:
				self.jatekos_nyert_egy_kort() if jatekos_pontjai > bot_pontjai else self.jatekos_vesztett_egy_kort()


	def jatekos_nyert_egy_kort(self):
		self.felhasznalo.gyozelmek += 1
		print(f'Gratulalok! Nyertel egy kort!\n')
		print(f'Bot/Te: {self.bot.gyozelmek}/{self.felhasznalo.gyozelmek} nyert kor\n')
		self.start_game()


	def jatekos_vesztett_egy_kort(self):
		self.bot.gyozelmek += 1
		print(f'Szomoru.. Vesztettel egy kort!\n')
		print(f'Bot/Te: {self.bot.gyozelmek}/{self.felhasznalo.gyozelmek} nyert kor\n')
		self.start_game()


	"""
	Osszegzi a jatekos/bot kezben levo kartyainak osszpontszamat
	:param kartyak: egy lista benne a jatekos kezeben levo kartyakkal
	:return: kartyak osszpontszama
	"""
	def pontok(self, kartyak):
		p = 0
		for kartya in kartyak:
			if kartya.ertek.value == 14:
				if p >= 11:
					p += 1
				else:
					p += 11
			elif 10 < kartya.ertek.value < 14:
				p += 10
			else:
				p += kartya.ertek.value
		return p


	def jatek_vege(self):
		print('---------------\nVege a jateknak!')
		print(f'{self.felhasznalo.nev} gyozelmei: {self.felhasznalo.gyozelmek}')
		print(f'Bot gyozelmei: {self.bot.gyozelmek}\n---------------')
		quit()



if __name__ == '__main__':
	nev = input('Add meg a neved: ')
	jatek = BlackJack(nev)

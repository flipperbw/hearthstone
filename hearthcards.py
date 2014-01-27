#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
from time import sleep
import re
import csv

fh = open('allcards.psv', 'a')

writer = csv.writer(fh, delimiter='|', lineterminator='\n')
writer.writerow(('cardname, cardlink', 'cardtype', 'cardclass', 'manacost', 'attack', 'health', 'rarity', 'cardset', 'faction', 'craftcost', 'craftcostgold', 'dust', 'dustgold', 'img', 'imggold', 'cardtext', 'flavortext', 'deckusage', 'arenausage', 'druid', 'hunter', 'mage', 'paladin', 'priest', 'rogue', 'shaman', 'warlock', 'warrior'))

for i in range(3,5):
	print '-> Page %s' % i
	cardlist = BeautifulSoup(requests.get('http://www.hearthpwn.com/cards?display=1&page=%s' % i).text)
	
	for card in cardlist.find('div', {'class':'listing-body'}).find('tbody').find_all('tr'):
		cols = card.find_all('td')
		
		cardname = cols[0].text.strip()
		cardlink = 'http://www.hearthpwn.com' + cols[0].find('a').get('href')
		cardtype = cols[1].text.strip()
		cardclass = cols[2].text.strip()
		if not cardclass:
			cardclass = 'N/A'
		manacost = cols[3].text.strip()
		attack = cols[4].text.strip()
		health = cols[5].text.strip()

		if cardtype in ('Hero', 'Hero Power'):
			pass
		else:
			carddata = BeautifulSoup(requests.get(cardlink).text)

			rarity = cardset = faction = race = craftcost = craftcostgold = dust = dustgold = deckusage = arenausage = img = imggold = cardtext = flavortext = druid = hunter = mage = paladin = priest = rogue = shaman = warlock = warrior = 'N/A'

			try:
				infobox = carddata.find('aside', {'class':'infobox'})
				textbox = carddata.find('div', {'class':'card-info'})
				flavorbox = carddata.find('div', {'class':'card-flavor-text'})
				imgbox = carddata.find('div', {'class':'hearth-tooltip'})
				imggoldbox = carddata.find('div', {'class':['hearth-tooltip', 'golden']})
				
				bullets = infobox.find_all('li')
				for b in bullets:
					bt = b.text
					if 'Rarity: ' in bt:
						rarity = b.find('a').text.strip()
					elif 'Set: ' in bt:
						cardset = b.find('a').text.strip()
					elif 'Race: ' in bt:
						race = b.find('a').text.strip()
					elif 'Faction: ' in bt:
						faction = b.find('a').find('span').text.strip()
					elif 'Crafting Cost: ' in bt:
						craftcost, craftcostgold = re.findall(r'\d+', bt)
					elif 'Arcane Dust: ' in bt:
						dust, dustgold = re.findall(r'\d+', bt)

				deckstat = carddata.find(text='Overall Deck Statistics')
				if deckstat:
					deckusage = re.findall(r'[\d.]+', deckstat.next.strip())[0]

				arenastat = carddata.find(text=re.compile('Picked.*of the time in Arena'))
				if arenastat:
					arenausage = re.findall(r'[\d.]+', arenastat.strip())[0]

				if imgbox:
					img = imgbox.find('img').get('src')
				if imggoldbox:
					imggold = imggoldbox.find('img').get('src')

				if textbox:
					cardtext = textbox.find('p').text.strip().encode('utf-8')
				if flavorbox:
					flavortext = flavorbox.find('p').text.strip().encode('utf-8')

				chart = infobox.find('script')
				if chart:
					chart = chart.text
					dists = re.findall(r"\['\w+', [\d.]+", chart)
					for dist in dists:
						dlist = dist.split(',')
						dname = re.sub('[[\']', '', dlist[0])
						ddist = str(round(float(re.sub('[ \]]', '', dlist[1])), 2))

						if dname == 'Druid':
							druid = ddist
						elif dname == 'Hunter':
							hunter = ddist
						elif dname == 'Mage':
							mage = ddist
						elif dname == 'Paladin':
							paladin = ddist
						elif dname == 'Priest':
							priest = ddist
						elif dname == 'Rogue':
							rogue = ddist
						elif dname == 'Shaman':
							shaman = ddist
						elif dname == 'Warlock':
							warlock = ddist
						elif dname == 'Warrior':
							warrior = ddist

			except:
				print('Issue getting card data: %s' % cardlink)

			else:
				writer.writerow((cardname, cardlink, cardtype, cardclass, manacost, attack, health, rarity, cardset, faction, craftcost, craftcostgold, dust, dustgold, img, imggold, cardtext, flavortext, deckusage, arenausage, druid, hunter, mage, paladin, priest, rogue, shaman, warlock, warrior))

	sleep(3)

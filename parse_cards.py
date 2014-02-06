#!/usr/bin/env python

from bs4 import BeautifulSoup
import glob
import json

#cd ~/dev/hearth
#cp /media/sf_hearth/cardxml0.unity3d .
#java -jar ~/disun/disunity.jar -f TextAsset ./cardxml0.unity3d

# ./parse_cards.py | python -mjson.tool

cards = {}

for f in glob.glob('cardxml0/TextAsset/*txt'):
	with open(f) as cardfile:
		cardsoup = BeautifulSoup(cardfile.read(), features="xml")

	card = cardsoup.find('Entity')

	"""
	collect = card.find('Tag', {'name':'Collectible'})
	if collect:
		collect = collect.get('value')
	if collect != '1':
		pass
	else:
	"""

	cardId = card.get('CardID')
	cards[cardId] = {}

	tags = card.find_all('Tag')
	for tag in tags:
		tagval = False
		tagname = tag.get('name')
		if tag.get('type') == 'String':
			tagval = tag.find('enUS').text.encode('utf-8')
		elif tag.get('type') == 'Bool':
			if tag.get('value') == '1':
				tagval = True
		else:
			tagval = tag.get('value')

		if tagval:
			cards[cardId][tagname] = tagval

	power = card.find('Power')
	if power:
		requirements = power.find_all('PlayRequirement')
		powerval = {}
		for p in requirements:
			powerval[p.get('reqID')] = p.get('param')

		if powerval:
			cards[cardId]['Requirements'] = powerval

	entourage = card.find_all('EntourageCard')
	entourageval = []

	for e in entourage:
		entourageval.append(e.get('cardID'))

	if entourageval:
		cards[cardId]['Entourage'] = entourageval

	reference = card.find_all('ReferencedTag')
	referenceval = []

	for r in reference:
		if r.get('type') == 'Bool' and r.get('value') == '1':
			referenceval.append(r.get('name'))

	if referenceval:
		cards[cardId]['ReferencedTag'] = referenceval

print json.dumps(cards)

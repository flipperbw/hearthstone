#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
from time import sleep

cardlist = {}
gems = {"0":[], "1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7+":[]}
rarities = {'1': 'Free', '2': 'Comm', '3': 'Rare', '4': 'Epic', '5': 'Lege'}
deck_count = 0

f = open('hearth', 'w')
cardfile = open('hearth_cards', 'w')
gemfile = open('hearth_gems', 'w')

for i in range(0,30):
	f.write('-> Page %s\n' % i)
	try:
		alldecks = BeautifulSoup(requests.get('http://www.hearthpwn.com/decks?filter-deck-tag=1&filter-is-forge=2&page=%s&sort=-rating' % i).text)
	except:
		print cardlist
		print gems
		print deck_count

	for deck in alldecks.find('div', {'class':'listing-body'}).find('tbody').find_all('tr'):
		cols = deck.find_all('td')
		deck_link = 'http://www.hearthpwn.com' + cols[0].find('a').get('href')
		
		if int(cols[-1].find('abbr').get('data-epoch')) < 1388451854:
			f.write('Skipped\n')
		else:
			f.write('Deck #%s: %s\n' % (deck_count, deck_link))
			deck_page = cols[0].find('a').get('href')
			
			try:
				deck_info = requests.get('http://www.hearthpwn.com%s' % deck_page).text
			except:
				print 'Could not get deck'
				print cardlist
				print gems
				print deck_count
			
			deck_soup = BeautifulSoup(deck_info)
			decklist = deck_soup.find('div', {'class':'listing-body'})
			gemlist = deck_soup.find('ul', {'class':'deck-graph-bars'})
			
			deck_table = decklist.find('tbody').find_all('tr')
			if len(deck_table) == 1:
				f.write('Empty deck.\n')
			else:
				for card in deck_table:
					card_info = card.find('td')
					card_link = 'http://www.hearthpwn.com' + card_info.find('a').get('href')
					card_rarity = card_info.find('a').get('class')[0][-1]
					card_name = card_info.text.strip().split('\r')[0]
				
					if cardlist.get(card_name):
						cardlist[card_name]['count'] += 1
					else:
						cardlist[card_name] = {'count': 1, 'link': card_link, 'rarity': rarities.get(card_rarity)}
		
					cardfile.write('%s\n' % card_name)
				
				for gem in gemlist.find_all('li'):
					gemcount = int(gem.get('data-count'))
					gemtype = gem.get('id')[-1]
					if gemtype == '7':
						gemtype = '7+'
					gems[gemtype].append(gemcount)
					gemfile.write('%s,%s\n' % (gemtype, gemcount))
				
				deck_count += 1
	sleep(3)

print('Decks: %s' % deck_count)
print('Mana breakdown:')
for g in sorted(gems.items(), key=lambda y: y[0]):
	avg = round(sum(g[1])*1.0/len(g[1])*1.0, 1)
	print('  %s:\t%s' % (g[0], avg))

print('\n----------------\n')

maxlen = max([len(p) for p in cardlist.keys()])
sorted_cards = sorted(cardlist.items(), key=lambda t: t[1].get('count'), reverse=True)
for s in sorted_cards:
	pct = round(s[1].get('count')*1.0 / deck_count * 1.0, 3)*100
	print('{0:{1}}{6:9}{2:{3}}{4:3} ({5:4}%)'.format(s[0], maxlen + 5, s[1].get('link'), maxlen + 40, s[1].get('count'), pct, s[1].get('rarity')))

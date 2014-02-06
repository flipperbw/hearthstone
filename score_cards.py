#!/usr/bin/env python

from bs4 import BeautifulSoup
import glob
import json

#cd ~/dev/hearth
#cp /media/sf_hearth/cardxml0.unity3d .
#java -jar ~/disun/disunity.jar -f TextAsset ./cardxml0.unity3d

# ./parse_cards.py | python -mjson.tool

cards = {}

tag_trans = {
	'CardSet' = {
		'0':'INVALID',
		'1':'TEST_TEMPORARY',
		'2':'CORE',
		'3':'EXPERT1',
		'4':'REWARD',
		'5':'MISSIONS',
		'6':'DEMO',
		'7':'NONE',
		'8':'CHEAT',
		'9':'BLANK',
		'10':'DEBUG_SP',
		'11':'PROMO',
		'12':'FP1',
		'13':'PE1',
		'14':'FP2',
		'15':'PE2',
		'16':'CREDITS'
	},

	'CardType' = {
		'0':'INVALID',
		'1':'GAME',
		'2':'PLAYER',
		'3':'HERO',
		'4':'MINION',
		'5':'ABILITY',
		'6':'ENCHANTMENT',
		'7':'WEAPON',
		'8':'ITEM',
		'9':'TOKEN',
		'10':'HERO_POWER'
	},

	'Class' = {
		'0':'INVALID',
		'1':'DEATHKNIGHT',
		'2':'DRUID',
		'3':'HUNTER',
		'4':'MAGE',
		'5':'PALADIN',
		'6':'PRIEST',
		'7':'ROGUE',
		'8':'SHAMAN',
		'9':'WARLOCK',
		'10':'WARRIOR',
		'11':'DREAM'
	},

	'Faction' = {
		'0':'INVALID',
		'1':'HORDE',
		'2':'ALLIANCE',
		'3':'NEUTRAL'
	},

	'Race' = {
		'0':'INVALID',
		'1':'BLOODELF',
		'2':'DRAENEI',
		'3':'DWARF',
		'4':'GNOME',
		'5':'GOBLIN',
		'6':'HUMAN',
		'7':'NIGHTELF',
		'8':'ORC',
		'9':'TAUREN',
		'10':'TROLL',
		'11':'UNDEAD',
		'12':'WORGEN',
		'13':'GOBLIN2',
		'14':'MURLOC',
		'15':'DEMON',
		'16':'SCOURGE',
		'17':'MECHANICAL',
		'18':'ELEMENTAL',
		'19':'OGRE',
		'20':'PET',
		'21':'TOTEM',
		'22':'NERUBIAN',
		'23':'PIRATE',
		'24':'DRAGON'
	},

	'Rarity' = {
		'0':'INVALID',
		'1':'COMMON',
		'2':'FREE',
		'3':'RARE',
		'4':'EPIC',
		'5':'LEGENDARY'
	},

	'EnchantmentVisual' = {
		'0':'INVALID',
		'1':'POSITIVE',
		'2':'NEGATIVE',
		'3':'NEUTRAL'
	},

	#'AttackVisualType' = {}

	'PlayRequirement' = {
		'0':'NONE',
		'1':'MINION_TARGET',
		'2':'FRIENDLY_TARGET',
		'3':'ENEMY_TARGET',
		'4':'DAMAGED_TARGET',
		'5':'ENCHANTED_TARGET',
		'6':'FROZEN_TARGET',
		'7':'CHARGE_TARGET',
		'8':'TARGET_MAX_ATTACK',
		'9':'NONSELF_TARGET',
		'10':'TARGET_WITH_RACE',
		'11':'TARGET_TO_PLAY',
		'12':'NUM_MINION_SLOTS',
		'13':'WEAPON_EQUIPPED',
		'14':'ENOUGH_MANA',
		'15':'YOUR_TURN',
		'16':'NONSTEALTH_ENEMY_TARGET',
		'17':'HERO_TARGET',
		'18':'SECRET_CAP',
		'19':'MINION_CAP_IF_TARGET_AVAILABLE',
		'20':'MINION_CAP',
		'21':'TARGET_ATTACKED_THIS_TURN',
		'22':'TARGET_IF_AVAILABLE',
		'23':'MINIMUM_ENEMY_MINIONS',
		'24':'TARGET_FOR_COMBO',
		'25':'NOT_EXHAUSTED_ACTIVATE',
		'26':'UNIQUE_SECRET',
		'27':'TARGET_TAUNTER',
		'28':'CAN_BE_ATTACKED',
		'29':'ACTION_PWR_IS_MASTER_PWR',
		'30':'TARGET_MAGNET',
		'31':'ATTACK_GREATER_THAN_0',
		'32':'ATTACKER_NOT_FROZEN',
		'33':'HERO_OR_MINION_TARGET',
		'34':'CAN_BE_TARGETED_BY_SPELLS',
		'35':'SUBCARD_IS_PLAYABLE',
		'36':'TARGET_FOR_NO_COMBO',
		'37':'NOT_MINION_JUST_PLAYED',
		'38':'NOT_EXHAUSTED_HERO_POWER',
		'39':'CAN_BE_TARGETED_BY_OPPONENTS',
		'40':'ATTACKER_CAN_ATTACK',
		'41':'TARGET_MIN_ATTACK',
		'42':'CAN_BE_TARGETED_BY_HERO_POWERS',
		'43':'ENEMY_TARGET_NOT_IMMUNE',
		'44':'ENTIRE_ENTOURAGE_NOT_IN_PLAY',
		'45':'MINIMUM_TOTAL_MINIONS',
		'46':'MUST_TARGET_TAUNTER',
		'47':'UNDAMAGED_TARGET'
	}
}


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

	#elif attrname S== 'ReferencedTag':
		#referencedtagval = False



	#now update the values with the modifiers

print json.dumps(cards)

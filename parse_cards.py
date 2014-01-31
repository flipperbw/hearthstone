#!/usr/bin/env python

from bs4 import BeautifulSoup
import glob
import json

#cd ~/dev/hearth
#cp /media/sf_hearth/cardxml0.unity3d .
#java -jar ~/disun/disunity.jar -f TextAsset ./cardxml0.unity3d

#cat cardxml0/TextAsset/* | egrep '<Tag |<ReferencedTag |<PlayRequirement ' | sort | uniq -c

cards = {}

"""
tag_trans = {
	CardSet
	CardType
	Class
	Faction
	Race
	Rarity
	PlayRequirement
}
"""

for f in glob.glob('cardxml0/TextAsset/*txt'):
	with open(f) as cardfile:
		cardsoup = BeautifulSoup(cardfile.read(), features="xml")

	card = cardsoup.find('Entity')
	collect = card.find('Tag', {'name':'Collectible'})
	if collect:
		collect = collect.get('value')
	if collect != '1':
		pass

	else:
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

"""
	 22   <Tag name="Atk" enumID="47" type="Number" value="0" />
	 13   <Tag name="CardSet" enumID="183" type="CardSet" value="11" />
	 14   <Tag name="CardType" enumID="202" type="CardType" value="10" />
	 43   <Tag name="Class" enumID="199" type="Class" value="10" />
	 60   <Tag name="Cost" enumID="48" type="Number" value="0" />
	  1   <Tag name="Durability" enumID="187" type="Number" value="1" />
	 20   <Tag name="Faction" enumID="201" type="Faction" value="1" />
	 62   <Tag name="Health" enumID="45" type="Number" value="1" />
	 11   <Tag name="Race" enumID="200" type="Race" value="24" />
	 58   <Tag name="Rarity" enumID="203" type="Rarity" value="5" />
	101   <Tag name="DevState" enumID="268" type="DevState" value="2" />
	  9   <Tag name="Recall" enumID="215" type="Number" value="1" />


	  2   <Tag name="AdjacentBuff" enumID="350" type="Bool" value="1" />
	  3   <Tag name="AffectedBySpellPower" enumID="370" type="Bool" value="1" />
	 14   <Tag name="Aura" enumID="362" type="Bool" value="1" />
	 78   <Tag name="Battlecry" enumID="218" type="Bool" value="1" />
	 18   <Tag name="Charge" enumID="197" type="Bool" value="1" />
	392   <Tag name="Collectible" enumID="321" type="Bool" value="1" />
	  9   <Tag name="Combo" enumID="220" type="Bool" value="1" />
	 11   <Tag name="Deathrattle" enumID="217" type="Bool" value="1" />
	  7   <Tag name="Divine Shield" enumID="194" type="Bool" value="1" />
	 55   <Tag name="Elite" enumID="114" type="Bool" value="1" />
	  6   <Tag name="Enrage" enumID="212" type="Bool" value="1" />
	  9   <Tag name="Freeze" enumID="208" type="Bool" value="1" />
	  1   <Tag name="GrantCharge" enumID="355" type="Bool" value="1" />
	  1   <Tag name="HealTarget" enumID="361" type="Bool" value="1" />
	 29   <Tag name="Taunt" enumID="190" type="Bool" value="1" />
	 51   <Tag name="TriggerVisual" enumID="32" type="Bool" value="1" />
	  6   <Tag name="Windfury" enumID="189" type="Bool" value="1" />
	  5   <Tag name="ImmuneToSpellpower" enumID="349" type="Bool" value="1" />
	  3   <Tag name="Morph" enumID="293" type="Bool" value="1" />
	 19   <Tag name="OneTurnEffect" enumID="338" type="Bool" value="1" />
	  2   <Tag name="Poisonous" enumID="363" type="Bool" value="1" />
	 15   <Tag name="Secret" enumID="219" type="Bool" value="1" />
	  4   <Tag name="Silence" enumID="339" type="Bool" value="1" />
	  8   <Tag name="Spellpower" enumID="192" type="Bool" value="1" />
	  6   <Tag name="Stealth" enumID="191" type="Bool" value="1" />
	  1   <Tag name="Summoned" enumID="205" type="Bool" value="1" />


	385   <Tag name="ArtistName" enumID="342" type="String">
	712   <Tag name="CardName" enumID="185" type="String">
	636   <Tag name="CardTextInHand" enumID="184" type="String">
	 46   <Tag name="CardTextInPlay" enumID="252" type="String">
	383   <Tag name="FlavorText" enumID="351" type="String">
	 92   <Tag name="HowToGetThisCard" enumID="364" type="String">
	137   <Tag name="HowToGetThisGoldCard" enumID="365" type="String">
	 32   <Tag name="TargetingArrowText" enumID="325" type="String">


		  <EntourageCard cardID="DREAM_01" />


	  1   <Power definition="00000012-63d5-47c6-a508-76da1ed8d507" />
	  1     <PlayRequirement reqID="10" param="14" />
	  1     <PlayRequirement reqID="10" param="15" />
	  2     <PlayRequirement reqID="10" param="20" />
	112     <PlayRequirement reqID="11" param="" /> #something for spells.(only card type 5 and 10)
	  9     <PlayRequirement reqID="12" param="1" /> #minion spots open?
	  1     <PlayRequirement reqID="12" param="2" />
	  2     <PlayRequirement reqID="13" param="" />
	  8     <PlayRequirement reqID="17" param="" />
	  1     <PlayRequirement reqID="19" param="2" />
	 79     <PlayRequirement reqID="1" param="" /> #opponent has minion
	 30     <PlayRequirement reqID="22" param="" />
	  1     <PlayRequirement reqID="23" param="0" />
	  1     <PlayRequirement reqID="23" param="1" />
	  3     <PlayRequirement reqID="23" param="2" />
	  2     <PlayRequirement reqID="24" param="" />
	 14     <PlayRequirement reqID="2" param="" />
	 15     <PlayRequirement reqID="3" param="" />
	  1     <PlayRequirement reqID="41" param="5" />
	  1     <PlayRequirement reqID="41" param="7" />
	  1     <PlayRequirement reqID="44" param="" />
	  1     <PlayRequirement reqID="45" param="2" />
	  1     <PlayRequirement reqID="46" param="" />
	  1     <PlayRequirement reqID="47" param="" />
	  2     <PlayRequirement reqID="4" param="" />
	  1     <PlayRequirement reqID="8" param="2" />
	  2     <PlayRequirement reqID="8" param="3" /> #attack val <
	 11     <PlayRequirement reqID="9" param="" />


	  3   <ReferencedTag name="Cant Be Damaged" enumID="240" type="Bool" value="1" />
	  7   <ReferencedTag name="Charge" enumID="197" type="Bool" value="1" />
	  1   <ReferencedTag name="Counter" enumID="340" type="Bool" value="1" />
	  1   <ReferencedTag name="Deathrattle" enumID="217" type="Bool" value="1" />
	  3   <ReferencedTag name="Divine Shield" enumID="194" type="Bool" value="1" />
	  1   <ReferencedTag name="Recall" enumID="215" type="Number" value="1" />
	  5   <ReferencedTag name="Secret" enumID="219" type="Bool" value="1" />
	  3   <ReferencedTag name="Silence" enumID="339" type="Bool" value="1" />
	  1   <ReferencedTag name="Spellpower" enumID="192" type="Bool" value="1" />
	  3   <ReferencedTag name="Stealth" enumID="191" type="Bool" value="1" />
	 14   <ReferencedTag name="Taunt" enumID="190" type="Bool" value="1" />
	  3   <ReferencedTag name="Windfury" enumID="189" type="Bool" value="1" />
"""

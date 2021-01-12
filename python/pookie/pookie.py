import discord
import asyncio

import pickle

import string
import random
import math
import time
from collections import deque

TOKEN = '[TOKEN]'

client = discord.Client()

target_guild = 'Olympia International Cooperative Gaming Initiative'
target_channel = 'pookie-under-construction'
target_channel_id = 766392552957542420

leaderboard = None

# directory = '~/Documents/Text Files/Code Projects/Python/Discord Bots/pookie/'
directory = ''

with open(directory + 'pookie_leaderboard_pickle', 'rb') as file:
	leaderboard = pickle.load(file)

for item in leaderboard:
	print(item, ' ', leaderboard[item])



class Game:
	def __init__(self):
		self.members = {} #player : available chips
		self.afk = []
		self.round = None
		self.round_active = False
		self.lobby_message = ''
		self.player_list = ' -'
		self.afk = {}

	def join(self, player):
		player_chips = self.check_leaderboard_membership(player)
		self.members[player] = player_chips
		self.afk[player] = 0

	def leave(self, player):
		self.members.pop(player)
		self.afk.pop(player)

	def chip_count_message(self):
		message = ''
		for player in self.members:
			message += tag_user(player) + ' has ' + str(self.members[player]) + ' dookems.\n'
		return message

	def update_player_list(self):

		if (len(self.members) == 0):
			player_list = ' -'
		else:
			player_list = ''
			for player in self.members:
				player_list += tag_user(player) + ' ' + str(self.members[player]) + ' dookems\n'

		return player_list

	def check_leaderboard_membership(self, player):
		if (player.id in leaderboard):
			self.members[player] = leaderboard[player.id]['chips']
			print("Player: ", player.nick, player.id, ' in leaderboard:')
			print(leaderboard[player.id], "\n")
			pass
		else:
			leaderboard[player.id] = {}
			leaderboard[player.id]['bankroll'] = 10000
			leaderboard[player.id]['chips'] = 300
			leaderboard[player.id]['hands-played'] = 0
			print('Initiated player into leaderboard')
			self.members[player] = 300

		return leaderboard[player.id]['chips']


	async def send_lobby_animation(self):
			await animated_lobby()

	class Round_of_Play:

		def __init__(self):

			self.ante = 5
			self.bet_time = 12
			self.pot = 0
			self.community_number = None
			self.player_scores = {}
			self.p_numbers = {} #personal numbers
			self.round_active = False
			self.bets = {}  # player : amount in pot

			self.action = None

			self.current_betting_player = None
			self.highest_bet = self.ante  #highest amount of chips one player has in pot


		#####################################################################################

		def check_player_chips(self):
			for player in game.members:
				if (chips := game.members[player] < 1):
					leaderboard[player.id]['bankroll'] -= 300 - chips
					self.add_chips(player, 300 - chips)
					# game.members[player] += 300 - chips
					return 0

				if (chips := game.members[player] > 600):
					leaderboard[player.id]['bankroll'] += chips - 600
					self.add_chips(player, -(chips - 600))
					# game.members[player] -= chips - 600
					return 0


		def add_chips(self, player, amount, payout=False):
		
			chips = game.members[player]
		
			if (amount > chips):
				amount = chips
		
			leaderboard[player.id]["chips"] += amount
			game.members[player] += amount
			self.pot -= amount

			if (payout):
				return 0
			else:
				self.bets[player] -= amount

		async def send_personal_numbers(self):
			
			for player in game.members: #send personal numbers to players
		
				personal_number = random.randint(1, 1000)/100
				space = ' ' * 4
				message = '\n - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = \n'
				message += '\nYour personal number is\n\n**' + space + str(personal_number) + space
				message += '**\n\nYou have *' + str(game.members[player]) + '* dookems to bet.\n\n'
				message += ' - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = \n'
				await player.send(personal_number)

				self.player_scores[player] = personal_number
				self.p_numbers[player] = personal_number

		async def post_community_number(self):
			self.community_number = (random.randrange(1, 2000)/100)
			community_number_output = 'Community Number is: **' + str(self.community_number) + '**'
			await channel.send(community_number_output)
			for player in self.player_scores:

				if (self.player_scores[player] == self.community_number):
					self.player_scores[player] = math.inf

				else:
					score = self.player_scores[player]
					self.player_scores[player] = score / (abs(score - self.community_number))

		#####################################################################################

		async def call(self, player):

			obligation = self.highest_bet - self.bets[player]

			if (obligation > game.members[player]):
				# self.bets[player] += game.members[player]
				self.add_chips(player, -(obligation))
				# game.members[player] = 0
				# leaderboard[player.id]['chips'] = 0

			else:
				self.add_chips(player, -(obligation))
				# self.bets[player] += obligation
				# game.members[player] -= obligation

			self.action = 'call'
			self.current_betting_player = None
			print(player.name, ' called.')

		async def check(self, player):
			pass

		async def raise_(self, player, amount):
			print(player.name, ' raise amount: ', amount)
			#if insufficient chips to raise
			if (amount > game.members[player]):
				return await self.call(player)

			if (amount > self.pot):         #max raise
				amount = self.pot
				print('amount lowered to ', amount)

			if (amount < self.highest_bet): #min raise
				amount = self.highest_bet
				print('amount raised to ', amount)


			self.highest_bet += amount
			print(player.name, ' Raised ', amount)

			self.bets[self.current_betting_player] += amount
			self.pot += amount
			game.members[self.current_betting_player] -= amount
			self.action = 'raise'

			self.current_betting_player = None

		async def fold(self, player):
			print(player.name, ' folded')
			self.player_scores.pop(player)

			self.action = 'fold'
			self.current_betting_player = None

		async def payouts(self):
			payout_message = 'Payouts: \n'
			if (len(self.player_scores) == 1): #winner by folding
				highest_scoring_player = max(self.player_scores, key=self.player_scores.get)
				payout_message += tag_user(highest_scoring_player) + ' wins ' +  str(self.pot)

				self.add_chips(highest_scoring_player, self.pot, payout=True)
				# game.members[highest_scoring_player] += self.pot
				await channel.send(payout_message)

				return await self.end_round()

			while (self.pot > 0):

				payout = 0
				highest_scoring_player = max(self.player_scores, key=self.player_scores.get)
				pot_staked = self.bets[highest_scoring_player]

				for bettor in self.bets:

					if (pot_staked >= self.bets[bettor]):

						owed = self.bets[bettor]
						self.bets[bettor] -= owed

						self.pot -= owed
						payout += owed

					else:

						owed = self.bets[bettor] - pot_staked
						self.bets[bettor] -= owed

						self.pot -= owed
						payout += owed

				self.add_chips(highest_scoring_player, payout, payout=True)
				# game.members[highest_scoring_player] += payout
				payout_message += (tag_user(highest_scoring_player) + ' wins ' + str(payout))
				self.player_scores.pop(highest_scoring_player)

			await channel.send(payout_message)

			return await self.end_round()

		async def end_round(self):
			for player in list(game.afk.keys()):
				if (game.afk[player] > 1):
					game.leave(player)

			game.round_active = False

			for player in self.player_scores.keys():
				leaderboard[player.id]['hands-played'] += 1

			#pickle leaderboard # # # # # # # # # #
			filename = 'pookie_leaderboard_pickle'
			with open(filename, 'wb') as file:
				pickle.dump(leaderboard, file)
			filename = 'leaderboard_pickle_backup'
			with open(filename, 'wb') as file:
				pickle.dump(leaderboard, file)
			# # # # # # # # # # # # # # # # # # # #



			return await game.send_lobby_animation()


		async def functional_betting(self, players, first_bet=True):

			print(' = - = - = - = - = - = - = - in functional_betting() = - = - = - = - = - = - = - = -')

			if (len(self.player_scores) == 1): #all but one player folded (set to zero for singleplayer)
					self.current_betting_player = None
					print('Only one player left in hand, calling self.payouts()')
					return 'end_early'

			if (not first_bet):

				next_bettors = players[0:-1]
			else: #if folded
				next_bettors = players[:]

			for player in next_bettors:

				action = await self.get_player_action(player)

				if (action == 'call'):
					pass

				else:

					after_player_index  = players[ players.index(player)+1:]
					before_player_index = players[:players.index(player)+1 ]
					new_player_order = after_player_index + before_player_index
		
					if (action == 'raise'):
						
						return await self.functional_betting(new_player_order, first_bet=False)
		
					if (action == 'fold'):
		
						new_player_order.remove(player)
						return await self.functional_betting(new_player_order, first_bet=False)

			after_player_index  = players[ players.index(player)+1:]
			before_player_index = players[:players.index(player)+1 ]
			new_player_order = after_player_index + before_player_index
			return new_player_order

		async def get_player_action(self, player):
			# # Prepare betting message to send to Discord Client # # # # # # # # # # # # # # # # # #
			obligation_int = self.highest_bet - self.bets[player]

			obligation_str = ' ' + str(obligation_int) + ' to `call`'
			pot_str = 'Pot is ' + str(self.pot)
			output = 'Action on ' +  tag_user(player) + ' | ' + pot_str + ' | ' + obligation_str + ' | '
			output_line_2 = '\n Min `raise` is: ' + str(self.highest_bet) + ' | Max `raise` is: ' + str(self.pot)

			self.action = None
			self.current_betting_player = player

			bet_time = 30
			time_spent = 0
			action_message = await channel.send(output + str(bet_time))
			await action_message.edit(content=output + str(bet_time - time_spent) + output_line_2)

			# await self.query_player_input(player)

			#While loop serves as a timer, when player acts the first condition will fail.
			while (player == self.current_betting_player and time_spent < bet_time):

				time_spent += 1
				await asyncio.sleep(1)
				await action_message.edit(content=output + str(bet_time - time_spent) + output_line_2)

			#Forces player choice if they don't decide before timer expires.
			#self.current_betting_player equals None after they act.
			if (player == self.current_betting_player):

				tag = tag_user(player)

				#Player checks (call) by default
				if (obligation_int == 0):
					await self.call(player)
					action = ('call')
					await channel.send(tag + ' Timed out and checked automatically.')

				#Player folds by default
				else:
					await self.fold(player)
					action = ('fold')
					await channel.send(tag + ' Timed out and folded automatically.')

				game.afk[player] += 1

			else:
				game.afk[player] = 0

			print('returning action: ', self.action)
			return self.action

		async def start_round_func(self, players=None):

			game.round_active = True

			for player in game.members:

				game.check_leaderboard_membership(player)
				self.bets[player] = 0
				self.add_chips(player, - (self.ante))

			await self.send_personal_numbers()

			round_start_message = ''
			for player in game.members:
				round_start_message += tag_user(player) + ' '

			await channel.send(round_start_message + 'in a pot worth ' + str(self.pot))

			inital_bettors = list(game.members.keys())

			bettors = await self.functional_betting(inital_bettors)
			if (bettors == 'end_early'):
				return await self.payouts()

			await self.post_community_number()

			final_bettors = await self.functional_betting(bettors)
			if (final_bettors == 'end_early'):
				return await self.payouts()

			return await self.payouts()

		#######################################################################################


def tag_user(user_object):
	return '<@' + str(user_object.id) + '>'

game = Game() ; print('game initialized')
# time.sleep(2)

channel = None

async def animated_lobby():

	colors = [':white_large_square:', ':red_square:', ':blue_square:', ':yellow_square:', ':green_square:', ':purple_square:']
	d_colors = deque(colors)
	d_r_colors = deque(reversed(colors))
	top_bar = ''.join(d_colors)
	bottom_bar = ''.join(d_r_colors)
	title = [':regional_indicator_p:', ':regional_indicator_o:', ':regional_indicator_o:', ':regional_indicator_k:', ':regional_indicator_i:', ':regional_indicator_e:']
	message = top_bar + '\n' + ''.join(title) + '\n' + bottom_bar

	send = await channel.send(message)
	game.lobby_message = await channel.send('Type `join`, then `start` to play. DM me `leaderboard` to see it. \nLet me ( <@249414104102600704> ) know if you run into any problems. \n **Players...**')

	game.player_list = await channel.send(game.update_player_list())

	while (not game.round_active):
		await asyncio.sleep(1)
		d_colors.rotate(1)
		d_r_colors.rotate(-1)
		top_bar = ''.join(d_colors)
		bottom_bar = ''.join(d_r_colors)
		message = top_bar + '\n' + ''.join(title) + '\n' + bottom_bar
		await send.edit(content=message)

	return print('return from animated_lobby()')

def lowercase_clean_message(message):
	table = str.maketrans(dict.fromkeys(string.punctuation))
	clean_payload = message.translate(table)
	clean_payload = ''.join(i for i in clean_payload if not i.isdigit())
	clean_payload = clean_payload.replace(" ", "")
	return clean_payload

def numerical_clean_message(message):
	amount = ''.join(i for i in message if i.isdigit())
	if (amount == ''):
		return 0
	else:
		return int(amount)

def sort_leaderboard(leaderboard, skip_newbies=False):

	scores = []
	for player_id in leaderboard:

		if (skip_newbies and leaderboard[player_id]['hands-played'] < 12):
			continue

		user = '<@' + str(player_id) + '>'
		scores.append((user, leaderboard[player_id]['bankroll']))

	print(scores)
	scores.sort(key=lambda x: x[1], reverse=True)
	return scores

def compose_leaderboard(user_score_tuples, player=None):

	leaderboard_str = ''

	for pair in user_score_tuples[:30]:

		if (pair[0] == player):
			pass

		else:

			rank_number = str(user_score_tuples.index(pair)+1) + '. ' 
			stats = pair[0] + ' - ' + str(pair[1]) + '\n'
			leaderboard_str += rank_number + stats

	return leaderboard_str

async def send_leaderboard(player):
	user_score_tuples = sort_leaderboard(leaderboard)
	leaderboard_str = compose_leaderboard(user_score_tuples, player=player)
	return await player.send(leaderboard_str)

@client.event #Performs body when 'on_ready' is reached.
async def on_ready(): 

	global channel

	for guild in client.guilds:
		if (guild.name == target_guild):
			print('guild found')
			break

	for channel in guild.channels:
		if (channel.id == target_channel_id):
			print('channel found')
			print(channel.id)
			break

	return await animated_lobby()
	################################################################################################

@client.event
async def on_message(payload):
	
	global channel
	clean_payload = lowercase_clean_message(payload.content)
		
	if (isinstance(payload.channel, discord.channel.DMChannel)):
		print('dm recieved')
		is_leaderboard_request = clean_payload == 'leaderboard'
		if (is_leaderboard_request):
			return await send_leaderboard(payload.author)

	if (clean_payload == 'join'):

		if (payload.author in game.members): 
			return await payload.delete()
		
		game.join(payload.author)

		player_list = game.update_player_list()

		print(payload.author.name, ' joined the lobby.')
		print('Current players: ')
		for player in game.members:
			print(player.name)
		await game.player_list.edit(content=player_list)
		return await payload.delete()


	if (clean_payload == 'leave'):
		print(payload.content)
		game.leave(payload.author)

		player_list = game.update_player_list()
		await game.player_list.edit(content=player_list)

		# await payload.add_reaction(':wave:')
		print(payload.author.name, ' left the lobby.')
		print('Current players: ')
		for player in game.members:
			print(player.name)
		return await payload.delete()

	if (clean_payload == 'start'):

		if (payload.author not in game.members):
			game.join(payload.author)
			player_list = game.update_player_list()
			await game.player_list.edit(content=player_list)

		if (len(game.members) < 2):
			await channel.send('Not enough players to start.')
			return await payload.delete()

		print(payload.content)
		print('Starting game with: ')
		print(game.members)
		game.round = game.Round_of_Play()
		return await game.round.start_round_func()

	if (game.round_active):
	
		player = game.round.current_betting_player
		is_human_author = not payload.author.bot
	
		if (payload.author != player and is_human_author):
			return await payload.delete()
	
		else:
	
			if (clean_payload == 'call'):
				return await game.round.call(player)
			
			if (clean_payload == 'fold'):
				return await game.round.fold(player)
			
			if (clean_payload == 'raise'):
				print('in raise condition')
				amount = numerical_clean_message(payload.content)
				return await game.round.raise_(player, int(amount))
		
		if (clean_payload == 'hi stranger'):
			print(payload.content)
			return await payload.author.send('hi =)')
		
		if (payload.author.bot == False):
			print('deleting message from ', payload.author, ": ", payload.content)
			return await payload.delete()



client.run(TOKEN)

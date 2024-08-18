print(
	'🔄 Quick Assistant is loading...'
)
import discord, json, datetime, asyncio
from discord.ext import commands, tasks
def getJSONFile(
	file: str = 'Warns'
):
	return json.load(
		open(
			file if '.json' in file else file + '.json'
		)
	)
def saveJSONFile(
	dictionary: dict,
	file: str = 'warns',
	indent: int = 4
):
	json.dump(
		dictionary,
		open(
			file if '.json' in file else file + '.json',
			'w'
		),
		indent = indent
	)
def embed(
	author: discord.User,
	title: str = None,
	description: str = None,
	footerText: str = None,
	footerIconURL: str = None,
	color: int = 0x5865f2
):
	embed = discord.Embed()
	embed.set_author(
		name = authorName,
		url = authorURL,
		icon_url = authorIconURL
	)
	embed.title = title
	embed.description = description
	embed.set_footer(
		text = footerText,
		icon_url = footerIconURL
	)
QA = commands.Bot(
	command_prefix = None,
	owner_ids = [
		658717958784417812, #Salazar
		655263219459293210, #il798li
		641317480366604299 #C.Rainey
	],
	intents = discord.Intents.all(),
	case_insensitive = True
)
@QA.event
async def on_ready():
	print(
		'✅ Successfully logged in as {}!'.format(
			QA.user
		)
	)
@QA.event
async def on_message(
	message: discord.Message
):
	if message.author.id == 986713391110443028:
		return
	if message.guild != None:
		if message.channel.category.id != 1104998135908016198 or message.author.id == 986713391110443028:
			return
		if message.content.lower().startswith(
			'-p'
		):
			return await message.add_reaction(
				'🤐'
			)
		embed = discord.Embed()
		embed.description = message.content
		embed.color = 0x5865f2
		embed.set_author(
			name = message.author,
			url = 'https://discord.com/users/' + str(
				message.author.id
			),
			icon_url = message.author.avatar.url,
		)
		if message.attachments != []:
			for attachment in message.attachments:
				if attachment.filename.endswith(
					'.png'
				) or attachment.filename.endswith(
					'.jpg'
				) or attachment.filename.endswith(
					'jpeg'
				):
					embed.set_image(
						url = attachment.url
					)
					break
		userID = int(
			message.channel.name.split(
				'-'
			)[
				1
			]
		)
		user = QA.get_user(
			userID
		)
		if user == None:
			user = await QA.fetch_user(
				userID
			)
		await user.send(
			embed = embed
		)
		await message.add_reaction(
			'✅'
		)
		return
	await message.channel.trigger_typing()
	name = '📨・ticket-{}'.format(
		message.author.id
	)
	if discord.utils.get(
		QA.get_all_channels(),
		name = name
	) == None:
			category = QA.get_channel(
				1104998135908016198
			)
			channel = await category.create_text_channel(
				name = name
			)
			embed = discord.Embed()
			embed.description = 'React to this message with :no_entry_sign: to close the ticket.'
			embed.color = 0x5865f2
			embed.set_author(
				name = message.author,
				icon_url = message.author.avatar.url
			)
			closeTicket = await channel.send(
				#'@everyone',
				embed = embed
			)
			await closeTicket.add_reaction(
				'🚫'
			)
			await closeTicket.pin()
	channel = discord.utils.get(
		QA.get_all_channels(),
		name = '📨・ticket-{}'.format(
			message.author.id
		),
		category = QA.get_channel(
			1104998135908016198
		)
	)
	embed = discord.Embed()
	embed.set_author(
		name = message.author,
		icon_url = message.author.avatar.url
	)
	embed.description = message.content
	embed.color = 0x5865f2
	if message.attachments != []:
		for attachment in message.attachments:
			if attachment.filename.endswith(
				'.png'
			) or attachment.filename.endswith(
				'.jpg'
			) or attachment.filename.endswith(
				'jpeg'
			):
				embed.set_image(
					url = attachment.url
				)
				break
	await channel.send(
		embed = embed
	)
	embed.set_author(
		name = message.author,
		icon_url = message.author.avatar.url
	)
	await message.add_reaction(
		'✅'
	)
@QA.event
async def on_raw_reaction_add(
	payload
):
	if payload.event_type != 'REACTION_ADD' or payload.user_id == 986713391110443028:
		return
	channel = QA.get_channel(
		payload.channel_id
	)
	if channel == None or channel.category == None or channel.category.id != 1104998135908016198:
		return print(
			channel
		)
	message = await channel.fetch_message(
		payload.message_id
	)
	if message.author.id != 986713391110443028 or 'React to this message with ' not in message.embeds[
		0
	].description or str(
		payload.emoji
	) != '🚫':
		return
	#reactionUser = QA.get_user(
	#	payload.user_id
	#)
	#await message.add_reaction(
	#	'✅'
	#)
	#try:
	#	await QA.wait_for(
	#		'reaction_add',
	#		check = lambda reaction, user: str(
	#			reaction.emoji
	#		) == '✅' and user.id == 655263219459293210,
	#		timeout = 10
	#	)
	#except asyncio.TimeoutError:
	#	await message.clear_reactions()
	#	await message.add_reaction(
	#		'🚫'
	#	)
	#	return
	userID = message.channel.name.split(
		'-'
	)[
		1
	]
	messages = await message.channel.history(
		limit = 250
	).flatten()
	messages.remove(
		message
	)
	#client = QA.get_user(
	#	int(
	#		userID
	#	)
	#)
	#transcript = 'Transcript of a Ticket with ' + str(
	#	client
	#) + ' (' + str(
	#	client.id
	#) + ')' + '\n\n'
	#for historyMessage in messages:
	#	if historyMessage.author.id == QA.user.id:
	#		if historyMessage.embeds == []:
	#			continue
	#		transcript += str(
	#			client
	#		) + ' (' + str(
	#			client.id
	#		) + '): ' + historyMessage.embeds[
	#			0
	#		].description
	#		continue
	#	transcript += str(
	#		historyMessage.author
	#	) + ' (' + str(
	#		historyMessage.author.id
	#	) + '): ' + historyMessage.content
	#	transcript += '\n'
	#open(
	#	'transcript.txt',
	#	'w'
	#).write(
	#	transcript
	#)
	#await QA.get_channel(
	#	867581268568178708
	#).send(
	#	files = [
	#		discord.File(
	#			fp = open(
	#				transcript.t
	#			)
	#		)
	#	]
	#)
	await channel.delete()
	user = QA.get_user(
		int(
			userID
		)
	)
	moderator = QA.get_user(
		payload.user_id
	)
	embed = discord.Embed()
	embed.description = 'This ticket was closed by ' + moderator.mention + ' (' + str(
		moderator
	) + '). You can open a new ticket by sending a message to me.'
	embed.color = 0x5865f2
	embed.set_author(
		name = moderator,
		icon_url = moderator.avatar.url
	)
	await user.send(
		embed = embed
	)
	await moderator.send(
		'This is a transcript of the message that was sent to ' + user.mention + '.',
		embed = embed
	)
@QA.event
async def on_member_leave(
	member
):
	if member.guild.id != 746622891956764735:
		return
	def check(
		message: discord.Message
	):
		return message.author.id == member.id
	for categoryID in [
		746631968221036645,
		756168655691317296
	]:
		category = QA.get_category(
			categoryID
		)
		for channel in category.text_channels:
			await channel.purge(
				limit = 10000,
				check = check
			)
@QA.slash_command(
	name = 'warn',
	guild_ids = [
		746622891956764735
	],
	description = 'Warns a user for breaking advertising rules.',
	guild_only = True
)
async def warn(
	context,
	user: discord.Option(
		discord.Member,
		'Who do you want to warn?',
		name = 'user'
	),
	reason: discord.Option(
		str,
		'Why do you want to warn this user?',
		name = 'reason'
	)
):
	await context.defer(
		ephemeral = True
	)
	embed = discord.Embed(
		color = 0x5865f2
	)
	embed.set_author(
		name = context.author,
		icon_url = context.author.display_avatar.url
	)
	if context.guild.get_role(
		879179824692862976
	) not in context.author.roles:
		embed.description = 'You must be on the Quick Advertising staff team to warn members!'
		return await context.respond(
			embed = embed,
			ephemeral = True
		)
	warns = getJSONFile()
	userID = str(
		user.id
	)
	if userID not in warns:
		previousWarnings = 0
	else:
		previousWarnings = warns[
			userID
		]
	messagesDeleted = 0
	channels = []
	logs = []
	beforeTimestamp = datetime.datetime.now().timestamp() - 600
	async for log in context.guild.audit_logs(
		limit = 250,
		user = context.author,
		action = discord.AuditLogAction.message_delete
	):
		if log.target.id == user.id and log.created_at.timestamp() > beforeTimestamp:
			logs.append(
				log
			)
			messagesDeleted += log.extra.count
			if log.extra.channel not in channels:
				channels.append(
					log.extra.channel
				)
	class warningDescription:
		amount = ''
		channels = ''
	if messagesDeleted == 0:
		embed.description = 'You must delete some ads by ' + user.mention + ' that break the rules before warning them!'
		return await context.respond(
			embed = embed,
			ephemeral = True
		)
	if messagesDeleted == 1:
		warningDescription.amount = 'You had 1 advertisement deleted from '
	elif messagesDeleted >= 2:
		warningDescription.amount = 'You had {} advertisements deleted from '.format(
			messagesDeleted
		)
	if len(
		channels
	) == 1:
		warningDescription.channels = channels[
			0
		].mention
	elif len(
		channels
	) == 2:
		warningDescription.channels = channels[
			0
		].mention + ' and ' + channels[
			1
		].mention
	elif len(
		channels
	) >= 3:
		for channel in channels:
			if channel == channels[
				0
			]:
				warningDescription.channels += channel.mention
			elif channel == channels[
				-1
			]:
				warningDescription.channels += ', and ' + channel.mention
			else:
				warningDescription.channels += ', ' + channel.mention
	punishments = [
		'No punishments are applied for the first 5 warnings.',
		'No punishments are applied for the first 5 warnings.',
		'No punishments are applied for the first 5 warnings.',
		'No punishments are applied for the first 5 warnings.',
		'No punishments are applied for the first 5 warnings.',
		'You have been muted for 6 hours.',
		'You have been muted for 24 hours.',
		'You have been muted for 48 hours.',
		'You have been muted for 72 hours.',
		'You have been kicked from the server.'
	]
	punishment = punishments[
		previousWarnings
	]
	embed.description = '_ _\n**Warning ' + str(
		previousWarnings + 1
	) + '**\n' + warningDescription.amount + warningDescription.channels + '.\n\n**Reason**\n' + reason + '\n\n**Punishment**\n' + punishment + '\n_ _'
	embed.set_thumbnail(
		url = user.display_avatar.url
	)
	embed.set_footer(
		icon_url = 'https://images-ext-2.discordapp.net/external/_Ngc3Wn6BuBv3Z3J8YOQ0XQ7YVQXoyLb-ZzvcQd5Cec/%3Fsize%3D4096/https/cdn.discordapp.com/icons/746622891956764735/b4671dc61b3d52cb4e9b9ac2a3e8cea4.png',
		text = 'Thanks for choosing Quick Advertising!'
	)
	confirmEmbed = discord.Embed()
	confirmEmbed.color = 0x5865f2
	embed.set_author(
		name = '{} | {}'.format(
			context.author,
			context.author.id
		),
		icon_url = context.author.display_avatar.url
	)
	await QA.get_channel(
		1104855036586119249
	).send(
		user.mention,
		embed = embed
	)
	if 'You have been muted for ' in punishment:
		currentTimestamp = datetime.datetime.now().timestamp()
		muteTimes = {
			'6': 6,
			'7': 24,
			'8': 48,
			'9': 72
		}
		newTimestamp = currentTimestamp + muteTimes[
			str(
				previousWarnings + 1
			)
		] * 3600
		await user.timeout(
			datetime.datetime.fromtimestamp(
				newTimestamp
			)
		)
	elif punishment == 'You have been kicked from the server.':
		await user.send(
			embed = embed
		)
		await user.kick()
	elif punishment == 'You have been banned from the server.':
		await user.send(
			embed = embed
		)
		await user.ban()
	embed.description = 'Sucessfully warned ' + user.mention + '!'
	embed.remove_footer()
	warns[
		userID
	] = previousWarnings + 1
	saveJSONFile(
		warns
	)
	await context.respond(
		embed = embed,
		ephemeral = True
	)
@QA.slash_command(
	guild_ids = [
		746622891956764735
	],
	description = 'Bans a member from the server.',
	guild_only = True
)
async def ban(
	context,
	member: discord.Option(
		discord.Member,
		'Who do you want to ban?'
	),
	reason: discord.Option(
		str,
		'Why do you want to ban this user?',
		required = False
	)
):
	await context.defer(
		ephemeral = True
	)
	embed = discord.Embed()
	embed.color = 0x5865f2
	embed.set_author(
		name = context.author,
		icon_url = context.author.display_avatar.url
	)
	if context.channel.permissions_for(
		context.author
	).ban_members == False:
		embed.description = 'You do not have permission to ban members!'
		return await context.respond(
			embed = embed,
			ephemeral = True
		)
	if member.id == context.author.id:
		embed.description = 'You cannot ban yourself!'
	if member.top_role.position == context.author.top_role.position:
		embed.description = 'You cannot ban ' + member.mention + ' because they have the same rank as you!'
	elif member.top_role.position > context.author.top_role.position:
		embed.description = 'You cannot ban ' + member.mention + ' because they have a higher rank than you!'
	elif context.author.top_role.position > member.top_role.position:
		embed.description = member.mention + ' was successfully banned!'
		await member.ban(
			reason = reason
		)
	await context.respond(
		embed = embed
	)
@QA.slash_command(
	description = 'Checks the latency of the bot.',
	guild_ids = [
		746622891956764735,
		969037967098281985
	]
)
async def ping(
	context
):
	ping = round(
		QA.latency * 1000
	)
	embed = discord.Embed()
	embed.color = 0x5865f2
	embed.description = 'Pong! I responded in approximately ' + str(
		ping
	) + ' milliseconds!'
	embed.set_author(
		name = context.author,
		icon_url = context.author.display_avatar.url
	)
	await context.respond(
		embed = embed,
		ephemeral = True
	)
@QA.slash_command(
	guild_ids = [
		746622891956764735
	],
	description = 'Contacts a user through the support system.'
)
async def contact(
	context,
	userID: discord.Option(
		str,
		'What is the ID of the user that you want to contact?',
		name = 'user-id'
	)
):
	await context.defer(
		ephemeral = True
	)
	embed = discord.Embed()
	embed.color = 0x5865f2
	embed.description = 'You have been contacted through mod-mail by ' + context.author.mention + '. Any message or image DMed to me will be forwarded to the Quick Advertising staff team.'
	embed.set_author(
		name = context.author,
		icon_url = context.author.display_avatar.url
	)
	try:
		user = QA.get_user(
			int(
				userID
			)
		)
		await user.send(
			embed = embed
		)
	except:
		embed.description = 'I could not create a ticket for this user. They may have blocked me or you provided an invalid user ID.'
		return await context.respond(
			embed = embed,
			ephemeral = True
		)
	tickets = QA.get_channel(
		1104998135908016198
	)
	ticket = await tickets.create_text_channel(
		name = '📨・ticket-' + str(
			user.id
		),
		reason = '{} ({}) contacted {} ({}).'.format(
			context.author,
			context.author.id,
			user,
			user.id
		)
	)
	embed.description = 'React to this message with :no_entry_sign: to close the ticket.'
	embed.set_author(
		name = user,
		icon_url = QA.get_guild(
			746622891956764735
		).get_member(
			user.id
		).display_avatar.url
	)
	closeTicket = await ticket.send(
		context.author.mention + ', make sure to ping @@everyone if you need to!',
		embed = embed
	)
	await closeTicket.add_reaction(
		'🚫'
	)
	await closeTicket.pin()
	embed.set_author(
		name = context.author,
		icon_url = context.author.display_avatar.url
	)
	embed.description = 'Successfully created a ticket for ' + user.mention + ' at ' + ticket.mention + '!'
	await context.respond(
		embed = embed,
		ephemeral = True
	)
@QA.slash_command(
	name = 'user-info',
	description = 'Checks the information about a Discord user.',
	guild_ids = [
		969037967098281985,
		746622891956764735
	]
)
async def userInfo(
	context,
	user: discord.Option(
		discord.Member,
		'Who do you want to check the information about?',
		default = None
	)
):
	await context.defer(
		ephemeral = True
	)
	embed = discord.Embed()
	embed.color = 0x5865f2
	embed.set_author(
		name = context.author.name,
		icon_url = context.author.display_avatar.url
	)
	user = context.author if user == None else user
	embed.set_thumbnail(
		url = user.display_avatar.url
	)
	nickname = '\n'
	if user.nick != None:
		nickname += 'Nickname: {}\n'.format(
			discord.utils.escape_markdown(
				user.nick
			)
		)
	embed.description = f'\nUsername: {user.name}\nDisplay Name: {user.display_name}\nNickname: {user.nick}\nID: {user.id}\nHighest Role: {user.top_role.mention}\nTotal Roles: {len(user.roles)}\nAccount Created: <t:{round(user.created_at.timestamp())}:R>\nAccount Joined: <t:{round(user.joined_at.timestamp())}:R>'
	await context.respond(
		embed = embed
	)
async def interaction(
	interaction
):
	if interaction.custom_id == 'disable_ping':
		pass
	if interaction.custom_id != 'checkin':
		return
	now = datetime.datetime.now()
	checkinExpired = round(
		now.timestamp()
	) + 300
	embed = discord.Embed()
	embed.color = 0x5865f2
	embed.set_author(
		name = interaction.user,
		icon_url = interaction.user.display_avatar.url
	)
	embed.description = 'You successfully checked in! Come back <t:{}:R> to check-in again.'.format(
		checkinExpired
	)
	view = discord.ui.View()
	view.add_item(
		discord.ui.Button(
			style = discord.ButtonStyle.primary,
			label = 'Disable Ping',
			custom_id = 'disable_ping'
		)
	)
	await interaction.response.send_message(
		embed = embed,
		ephemeral = True,
		delete_after = 300
	)
@QA.slash_command(
	description = 'Gets a user\'s avatar.',
	guild_ids = [
		969037967098281985,
		746622891956764735
	],
)
async def avatar(
	context,
	user: discord.Option(
		discord.Member,
		'Whose avatar do you want to view?',
		default = None
	),	
	format: discord.Option(
		str,
		'Do you have a prefered encoding format for the image file? Leave this blank for PNG.',
		choices = [
			discord.OptionChoice(
				'PNG'
			),
			discord.OptionChoice(
				'JPG'
			),
			discord.OptionChoice(
				'WEBP'
			)
		],
		default = 'PNG'
	)
):
	await context.defer(
		ephemeral = True
	)
	if user == None:
		user = context.author
	embed = discord.Embed()
	embed.color = 0x5865f2
	embed.set_author(
		name = context.author,
		icon_url = context.author.display_avatar.with_format(
			format.lower()
		).url,
		url = 'https://discord.com/users/' + str(
			context.author.id
		)
	)
	embed.set_image(
		url = context.author.display_avatar.with_format(
			format.lower()
		).url
	)
	embed.title = user.name + '\'s Avatar'
	view = discord.ui.View()
	view.add_item(
		discord.ui.Button(
			label = 'Open in Browser',
			style = discord.ButtonStyle.link,
			url = context.author.display_avatar.with_format(
				format.lower()
			).url
		)
	)
	await context.respond(
		embed = embed,
		view = view
	)
@QA.slash_command(
	name = 'add-offline-warns',
	description = 'Adds warns to users that were warned while Quick Assistant was offline.',
)
async def add_offline_warns(
	context,
	user: discord.Option(
		discord.Member,
		description = 'Who was warned while Quick Assistant was offline?'
	),
	amount: discord.Option(
		int,
		description = 'How many times was this user warned while Quick Assistant was offline?',
		default = 1
	)
):
	
	await context.defer(
		ephemeral = True
	)
	warns = getJSONFile()
	userID = str(
		user.id
	)
	if userID not in warns:
		warns[
			userID
		] = 0
	warns[
		userID
	] += amount
	saveJSONFile(
		warns
	)
	embed = discord.Embed()
	embed.description = 'Successfully added {} {} to {}!'.format(
		amount,
		'warn' if amount == 1 else 'warns',
		user.mention
	)
	embed.set_thumbnail(
		url = user.avatar.url
	)
if False:
	@QA.slash_command(
		name = 'search-for-channels',
		description = 'Searches Quick Advertising\'s channels for ones that have your query in their name.',
		guild_ids = [
			746622891956764735
		]
	)
	async def search_for_channels(
		context,
		query: discord.Option(
			input_type = str,
			description = 'What does your target channel have in its name?',
		)
	):
		await context.defer(
			ephemeral = True
		)
		channels = []
		for channel in context.guild.text_channels:
			if query in channel.name:
				channels.append(
					channel
				)
		embed = discord.Embed()
		embed.color = 0x5865f2
		embed.title = 'Found ' + str(
			len(
				channels
			)
		) + ' channels:'
		for channel in channels:
			embed.description += channel.mention + ', ' + channel.category.name
			embed.description += '\n' if channel != channels[
				-1
			] else ''
		embed.set_author(
			name = str(

			),
			icon_url = context.aythor.display_avatar.url,
			url = 'https://discord.com/users/' + str(
				context.author.id
			),
		)
		await context.respond(
			embed = embed,
			ephemeral = True
		)
@tasks.loop(
	minutes = 1
)
async def staffList():
	hierarchy = {
	}
	guild = QA.get_guild(
		746622891956764735
	)
	channel = QA.get_channel(
		1109911384180928564
	)
	print(channel.name)
	message = await channel.fetch_message(
		1109912167731437729
	)
	string = 'Board of Directors: '
	members = []
	for role in filter(
		lambda role: 'Board ' in role.name,
		guild.roles[
			::-1
		]
	):
		print('- Role', role.name)
		for member in role.members:
			print(member.name)
			if member not in members:
				string += member.mention + ' '
				members.append(
					member
				)
	await message.edit(
		string
	)
QA.run(
	open(
		'Secrets/Token.txt'
	).read()
)
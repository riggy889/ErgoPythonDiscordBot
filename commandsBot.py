import hikari
import lightbulb
import ergo
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

bot = lightbulb.BotApp(
    token=TOKEN,
    default_enabled_guilds=(int(GUILD_ID))
)


@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started')


@bot.command
@lightbulb.command('ping', 'Says pong!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond('Pong!')


# Ergo Bot Command - Get AddressByTokenID
@bot.command()
@lightbulb.option('tokenid', 'Enter a token id here:')
@lightbulb.command('returnaddressbytokenid', 'Returns address where the token id lives...')
@lightbulb.implements(lightbulb.SlashCommand)
async def returnaddressbytokenid(ctx):
    ergoAddress = ergo.GetAddressByTokenID(ctx.options.tokenid)
    await ctx.respond('TokenID <' + ctx.options.tokenid + '> lives in this ergo address -' + ergoAddress)


# Ergo Bot Command - Get Current Ergo Price
@bot.command()
@lightbulb.command('getcurrentergoprice', 'Returns Current Ergo Price (Source - Coin Gecko)')
@lightbulb.implements(lightbulb.SlashCommand)
async def getcurrentergoprice(ctx):
    ergoPrice = ergo.GetCurrentPriceForErgo()
    await ctx.respond('Current Ergo Price - $' + str(ergoPrice))


# Ergo Bot Command - Get Tokens for Address
@bot.command()
@lightbulb.option('address', 'Enter your address here:')
@lightbulb.command('returntokensbyaddress', 'Returns tokens from your address balance...')
@lightbulb.implements(lightbulb.SlashCommand)
async def returntokensbyaddress(ctx):
    dataValues = ergo.GetTokensFromAddress(ctx.options.address)
    ergoBalance = str(dataValues[0] / 1000000000)
    tokenList = dataValues[1]
    await ctx.respond('Ergo Balance in Address - '+ergoBalance+' ERG')
    await ctx.respond('Tokens in Wallet: ')
    for token in tokenList:
        await ctx.respond('- '+token)


bot.run()

# disembedbuilder
Simple embed builder made with modals and buttons

# Installation
```
pip install disembedbuilder
```

### Attention !
You need to use py-cord 2.3.X or higher (3.X not supported)
Works only with slash commands

# Parameters

|           Name             |                     Type                     |Default|                           Information                               |
|:-------------------------:|:-------------------------------------------:|:----------:|:-------------------------------------------------------------------:|
|           ctx             | `discord.ApplicationContext` |            |                                                                     |
| timeout `<optional>`|                    `int`                   |   `180`  | Timeout for deleting or disabling menu |
|   delete_on_timeout `<optional>`   |                    `bool`                   |   `False`  |      Delete menu on timeout      |

# Methods

### start - sends the menu

# Usage example

```py
import discord
from discord import slash_command
from discord.ext import commands
import disembedbuilder

client = commands.Bot(command_prefix='YOUR_PREFIX_HERE', intents=discord.Intents.all())
client.remove_command('help')

class JustACog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="Simple embed builder with menu")
    async def embedbuilder(self, ctx):
        builder = disembedbuilder.EmbedBuilder(ctx, timeout=1800, delete_on_timeout=False)
        await builder.start()

client.add_cog(JustACog(client))
client.run("YOUR_TOKEN_HERE")
```


import datetime
import json
import os
import discord.errors
from discord.ui import View, Modal, InputText, Button, Select
from discord import ButtonStyle, InputTextStyle, Interaction, Embed, SelectOption, EmbedField
from typing import Union
from .preembeds import error_embed, info_embed, success_embed


class EmbedBuilder(View):
    def __init__(self,
                 ctx: discord.ApplicationContext,
                 timeout: Union[int, None] = 180,
                 delete_on_timeout: bool = False):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.user = ctx.author
        self.timeout = timeout
        self.embed = Embed(title="Embed builder", description=f"Use buttons below to edit your emb\nBuilder will {f'close automatically in `{timeout}` seconds' if timeout is not None else '**never closes** 💀'}", colour=int("2B2D31", 16))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user == self.user: return True
        return False

    # GENERAL SETTINGS | Title + Description + Color

    @discord.ui.button(label="⠀⠀⠀GENERAL⠀⠀", style=ButtonStyle.secondary, row=0, disabled=True)
    async def callback1(self): pass

    @discord.ui.button(label="⠀⠀Title⠀⠀", style=ButtonStyle.blurple, row=0)
    async def title_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the title", timeout=None)
        modal.add_item(InputText(label="Embed title", placeholder="Type here your embed title", required=False, max_length=256, value=self.embed.title if self.embed.title else ""))

        async def modal_callback(modal_interaction):
            new_title = modal_interaction.data["components"][0]["components"][0]["value"]
            self.embed.title = new_title if new_title != "" else None
            await interaction.edit_original_response(embed=self.embed)
            await modal_interaction.response.defer()

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)

    @discord.ui.button(label="⠀Description⠀", style=ButtonStyle.blurple, row=0)
    async def description_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the description", timeout=None)
        modal.add_item(InputText(label="Embed description", style=InputTextStyle.long, placeholder="Type here your embed description", required=True, min_length=1, max_length=4000, value=self.embed.description))

        async def modal_callback(modal_interaction):
            new_value = modal_interaction.data["components"][0]["components"][0]["value"]
            self.embed.description = new_value
            await interaction.edit_original_response(embed=self.embed)
            await modal_interaction.response.defer()

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)

    @discord.ui.button(label="⠀⠀⠀Color⠀⠀⠀", style=ButtonStyle.blurple, row=0)
    async def color_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the color", timeout=None)
        modal.add_item(InputText(label="Embed color", style=InputTextStyle.short, placeholder="Specify your embed color", required=True, min_length=6, max_length=6, value=hex(self.embed.colour.value)[2::].upper()))

        async def modal_callback(modal_interaction):
            new_value = modal_interaction.data["components"][0]["components"][0]["value"]
            if 0 <= int(new_value, 16) <= 16777215:
                self.embed.colour.value = int(new_value, 16)
                await interaction.edit_original_response(embed=self.embed)
                await modal_interaction.response.defer()
            else:
                await modal_interaction.response.send_message(embed=error_embed(f"{modal_interaction.user.mention}, incorrect HEX color code!"), ephemeral=True)

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)

    @discord.ui.button(label="⠀Title URL⠀", style=ButtonStyle.blurple, row=0)
    async def title_url_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the title", timeout=None)
        modal.add_item(InputText(label="Embed title url", style=InputTextStyle.short, placeholder="https://...", required=True, max_length=256, value=self.embed.url))

        async def modal_callback(modal_interaction):
            new_value = modal_interaction.data["components"][0]["components"][0]["value"]
            if new_value.startswith("http://") or new_value.startswith("https://"):
                self.embed.url = new_value
                await interaction.edit_original_response(embed=self.embed)
                await modal_interaction.response.defer()
            else:
                await modal_interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, invalid URL"), ephemeral=True)

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)



    # OPTIONAL SETTINGS | Author + Footer + Timestamp

    @discord.ui.button(label="⠀⠀OPTIONAL⠀⠀", style=ButtonStyle.secondary, row=1, disabled=True)
    async def callback2(self): pass

    @discord.ui.button(label="⠀Author⠀", style=ButtonStyle.blurple, row=1)
    async def author_name_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the author", timeout=None)
        modal.add_item(InputText(label="Embed author", style=InputTextStyle.short, placeholder="Type here author of embed", required=True, max_length=256, value=self.embed.author.name))

        async def modal_callback(modal_interaction):
            new_value = modal_interaction.data["components"][0]["components"][0]["value"]
            self.embed.set_author(name=new_value)
            await interaction.edit_original_response(embed=self.embed)
            await modal_interaction.response.defer()

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)

    @discord.ui.button(label="⠀⠀⠀Footer⠀⠀⠀", style=ButtonStyle.blurple, row=1)
    async def footer_text_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the footer", timeout=None)
        modal.add_item(InputText(label="Embed footer", style=InputTextStyle.long, placeholder="Type here footer of embed", required=True, max_length=2048, value=self.embed.footer.text))

        async def modal_callback(modal_interaction):
            new_value = modal_interaction.data["components"][0]["components"][0]["value"]
            self.embed.set_footer(text=new_value)
            await interaction.edit_original_response(embed=self.embed)
            await modal_interaction.response.defer()

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)

    @discord.ui.button(label="⠀Timestamp⠀", style=ButtonStyle.blurple, row=1)
    async def timestamp_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the timestamp", timeout=None)
        modal.add_item(InputText(label="Embed timestamp", style=InputTextStyle.long, placeholder="Type here timestamp of embed", required=True, min_length=10, max_length=10))

        async def modal_callback(modal_interaction):
            try:
                new_value = float(modal_interaction.data["components"][0]["components"][0]["value"])
                self.embed.timestamp = datetime.datetime.fromtimestamp(new_value)
                await interaction.edit_original_response(embed=self.embed)
                await modal_interaction.response.defer()
            except ValueError:
                await modal_interaction.response.send_message(embed=error_embed(f"{modal_interaction.user.mention}, timestamp should be in UNIX format!"), ephemeral=True)

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)

    @discord.ui.button(label="⠀⠀⠀⠀⠀⠀⠀⠀", style=discord.ButtonStyle.blurple, disabled=True, row=1)
    async def emptybutton2(self): pass

    # FIELDS SETTINGS | Add + Edit + Delete

    @discord.ui.button(label="⠀⠀⠀⠀FIELDS⠀⠀⠀", style=ButtonStyle.secondary, row=2, disabled=True)
    async def callback3(self): pass

    @discord.ui.button(label="⠀Add field", style=ButtonStyle.blurple, row=2)
    async def add_field_callback(self, button: Button, interaction: Interaction):
        if len(self.embed.fields) <= 25:
            modal = Modal(title="Adding the field", timeout=None)
            modal.add_item(InputText(label="Field name", style=InputTextStyle.long, required=True, max_length=256))
            modal.add_item(InputText(label="Field value", style=InputTextStyle.long, required=True, max_length=1024))
            modal.add_item(InputText(label="Inline display (True | False)", value="True", style=InputTextStyle.long, required=True, min_length=4, max_length=5))

            async def modal_callback(modal_interaction):
                data = modal_interaction.data["components"]
                field_name = data[0]["components"][0]["value"]
                field_value = data[1]["components"][0]["value"]
                field_inline = True if data[2]["components"][0]["value"].lower() == "true" else False
                self.embed.add_field(name=field_name, value=field_value, inline=field_inline)
                await interaction.edit_original_response(embed=self.embed)
                await modal_interaction.response.defer()

            modal.callback = modal_callback

            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, you have already added the maximum number of fields"), ephemeral=True)

    @discord.ui.button(label="⠀⠀Edit field⠀⠀", style=ButtonStyle.blurple, row=2)
    async def edit_field_callback(self, button: Button, interaction: Interaction):
        if len(self.embed.fields) >= 1:
            view_selector= View()
            selector = Select(placeholder="Choose field to edit", options=[SelectOption(label=v.name, value=str(k)) for k, v in enumerate(self.embed.fields)])
            view_selector.add_item(selector)

            async def select_callback(select_interaction):
                selected_index = selector.values[0]
                selected_field = self.embed.fields[int(selected_index)]
                await select_interaction.message.delete()

                modal = Modal(title="Editing the fields", timeout=None)
                modal.add_item(InputText(label="Field name", style=InputTextStyle.long, required=True, max_length=256, value=selected_field.name))
                modal.add_item(InputText(label="Field value", style=InputTextStyle.long, required=True, max_length=1024, value=selected_field.value))
                modal.add_item(InputText(label="Inline display (True | False)", style=InputTextStyle.long, required=True, min_length=4, max_length=5, value="True" if selected_field.inline else "False"))

                async def modal_callback(modal_interaction):
                    data = modal_interaction.data["components"]
                    field_name = data[0]["components"][0]["value"]
                    field_value = data[1]["components"][0]["value"]
                    field_inline = True if data[2]["components"][0]["value"].lower() == "true" else False
                    self.embed.fields[int(selected_index)] = EmbedField(name=field_name, value=field_value, inline=field_inline)

                    await self.message.edit(embed=self.embed)
                    await modal_interaction.response.defer()

                modal.callback = modal_callback

                await select_interaction.response.send_modal(modal)

            selector.callback = select_callback

            await interaction.response.send_message(view=view_selector)
        else:
            await interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, you have not added any field yet!"), ephemeral=True)

    @discord.ui.button(label="⠀Delete field⠀", style=ButtonStyle.blurple, row=2)
    async def delete_field_callback(self, button: Button, interaction: Interaction):
        if len(self.embed.fields) >= 1:
            view_selector= View()
            selector = Select(placeholder="Choose field to delete", options=[SelectOption(label=v.name, value=str(k)) for k, v in enumerate(self.embed.fields)])
            view_selector.add_item(selector)

            async def select_callback(select_interaction):
                selected_index = selector.values[0]
                self.embed.fields.pop(int(selected_index))
                await self.message.edit(embed=self.embed)
                await select_interaction.message.delete()

            selector.callback = select_callback
            await interaction.response.send_message(view=view_selector)
        else:
            await interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, you have not added any field yet!"), ephemeral=True)

    @discord.ui.button(label="⠀⠀⠀⠀⠀⠀⠀⠀", style=discord.ButtonStyle.blurple, disabled=True, row=2)
    async def emptybutton3(self): pass

    # IMAGES SETTINGS | Author image + Footer image + Thumbnail + Big image

    @discord.ui.button(label="⠀⠀⠀IMAGES⠀⠀⠀", style=ButtonStyle.secondary, row=3, disabled=True)
    async def callback4(self): pass

    @discord.ui.button(label="Author IMG", style=ButtonStyle.blurple, row=3)
    async def author_icon_callback(self, button: Button, interaction: Interaction):
        if self.embed.author.name:
            modal = Modal(title="Editing the author", timeout=None)
            modal.add_item(InputText(label="Embed author icon url", style=InputTextStyle.short, placeholder="https://...", required=True, max_length=256, value=self.embed.author.icon_url))

            async def modal_callback(modal_interaction):
                new_value = modal_interaction.data["components"][0]["components"][0]["value"]
                if new_value.startswith("http://") or new_value.startswith("https://"):
                    self.embed.set_author(icon_url=new_value, name=self.embed.author.name)
                    await interaction.edit_original_response(embed=self.embed)
                    await modal_interaction.response.defer()
                else:
                    await modal_interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, invalid URL"), ephemeral=True)

            modal.callback = modal_callback

            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, you need to set up author name first!"), ephemeral=True)

    @discord.ui.button(label="⠀Footer IMG⠀", style=ButtonStyle.blurple, row=3)
    async def footer_icon_callback(self, button: Button, interaction: Interaction):
        if self.embed.footer.text:
            modal = Modal(title="Editing the footer", timeout=None)
            modal.add_item(InputText(label="Embed footer icon url", style=InputTextStyle.short, placeholder="https://...", required=True, max_length=256, value=self.embed.footer.icon_url))

            async def modal_callback(modal_interaction):
                new_value = modal_interaction.data["components"][0]["components"][0]["value"]
                if new_value.startswith("http://") or new_value.startswith("https://"):
                    self.embed.set_footer(text=self.embed.footer.text, icon_url=new_value)
                    await interaction.edit_original_response(embed=self.embed)
                    await modal_interaction.response.defer()
                else:
                    await modal_interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, invalid URL"), ephemeral=True)

            modal.callback = modal_callback

            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, you need to set up footer text first!"), ephemeral=True)

    @discord.ui.button(label="⠀Thumbnail⠀", style=ButtonStyle.blurple, row=3)
    async def thumbnail_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the thumbnail", timeout=None)
        modal.add_item(InputText(label="Embed thumbnail icon url", style=InputTextStyle.short, placeholder="https://...", required=True, max_length=256, value=self.embed.thumbnail.url))

        async def modal_callback(modal_interaction):
            new_value = modal_interaction.data["components"][0]["components"][0]["value"]
            if new_value.startswith("http://") or new_value.startswith("https://"):
                self.embed.set_thumbnail(url=new_value)
                await interaction.edit_original_response(embed=self.embed)
                await modal_interaction.response.defer()
            else:
                await modal_interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, invalid URL"), ephemeral=True)

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)

    @discord.ui.button(label="⠀Big Image⠀", style=ButtonStyle.blurple, row=3)
    async def big_image_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Editing the big image", timeout=None)
        modal.add_item(InputText(label="Embed big image url", style=InputTextStyle.short, placeholder="https://...", required=True, max_length=256, value=self.embed.image.url))

        async def modal_callback(modal_interaction):
            new_value = modal_interaction.data["components"][0]["components"][0]["value"]
            if new_value.startswith("http://") or new_value.startswith("https://"):
                self.embed.set_image(url=new_value)
                await interaction.edit_original_response(embed=self.embed)
                await modal_interaction.response.defer()
            else:
                await modal_interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, invalid URL"), ephemeral=True)

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)


    # ACTIONS | POST + CANCEL + BACKUP + LOAD

    @discord.ui.button(label="⠀⠀⠀ACTIONS⠀⠀", style=ButtonStyle.secondary, row=4, disabled=True)
    async def callback5(self): pass

    @discord.ui.button(label="⠀Post⠀", style=ButtonStyle.green, row=4, emoji="📨")
    async def post_callback(self, button: Button, interaction: Interaction):
        modal = Modal(title="Post your embed", timeout=None)
        modal.add_item(InputText(label="Channel ID to post", style=InputTextStyle.short, required=True, min_length=18, max_length=19, value=self.ctx.channel.id))

        async def modal_callback(modal_interaction):
            new_value = modal_interaction.data["components"][0]["components"][0]["value"]
            channel = self.ctx.guild.get_channel(int(new_value))
            if channel:
                await channel.send(embed=self.embed)
                await modal_interaction.response.defer()
            else:
                await modal_interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, this channel ID does not belong to this guild or doesn't exist"), ephemeral=True)

        modal.callback = modal_callback

        await interaction.response.send_modal(modal)

    @discord.ui.button(label="⠀Disable⠀", style=ButtonStyle.red, row=4, emoji="🗑️")
    async def cancel_callback(self, button: Button, interaction: Interaction):
        await interaction.response.defer()
        for child in self.children:
            child.disabled = True
        await interaction.edit_original_response(embed=self.embed, view=self)
        self.stop()

    @discord.ui.button(label="⠀⠀Save⠀⠀", style=ButtonStyle.grey, row=4, emoji="💾")
    async def backup_callback(self, button: Button, interaction: Interaction):
        dictionary = self.embed.to_dict()
        dictionary.pop("type")
        content = f"Here is your backup! Save this content to any file\n\n```json\n{json.dumps(dictionary, ensure_ascii=True, indent=4)}```"
        await interaction.response.send_message(content)

    @discord.ui.button(label="⠀Load⠀⠀", style=ButtonStyle.grey, row=4, emoji="🔍")
    async def load_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_message(embed=info_embed(f"{interaction.user.mention}, send your backup file right here\nYou have `30` seconds"), ephemeral=True)

        try:
            def check(message):
                return (interaction.channel == message.channel) and (message.author == interaction.user)

            msg = await self.ctx.bot.wait_for("message", check=check, timeout=30)
            try:
                attachment = [_ for _ in msg.attachments][0]
                await attachment.save("backup.json")
                with open("backup.json", encoding='UTF-8') as file: dictionary = json.load(file)
                emb = Embed.from_dict(dictionary)
                os.remove("backup.json")
                self.embed = emb
                await self.message.edit(embed=self.embed)
                await interaction.followup.send(embed=success_embed(f"{interaction.user.mention}, your backup was successfully loaded"), ephemeral=True)
            except IndexError:
                await interaction.followup.send(embed=error_embed(f"{interaction.user.mention}, you didn't send the file"), ephemeral=True)
            except Exception as e:
                print(e)
                os.remove("backup.json")
                await interaction.followup.send(embed=error_embed(f"{interaction.user.mention}, file backup is not valid"), ephemeral=True)
            await msg.delete()

        except TimeoutError:
            await interaction.followup.send(embed=error_embed(f"{interaction.user.mention}, you didn't send the file in `30` seconds.\nPlease, try again"), ephemeral=True)

    async def start(self):
        await self.ctx.interaction.response.send_message(embed=self.embed, view=self)

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        self.message.edit(embed=self.embed, view=self)
        self.stop()

    async def on_check_failure(self, interaction: Interaction) -> None:
        await interaction.response.send_message(embed=error_embed(f"{interaction.user.mention}, you cannot interact with this menu!"), ephemeral=True)


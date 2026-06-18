import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ضع هنا رقم الرتبة التي سيحصل عليها العضو عند الموافقة
ROLE_ID = 1516227002170871848 

class AgreementView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="نعم ✅", style=discord.ButtonStyle.green, custom_id="agree_button")
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("تم قبول الشروط، أهلاً بك في Zone Store!", ephemeral=True)
        else:
            await interaction.response.send_message("خطأ: الرتبة غير موجودة، تواصل مع الإدارة.", ephemeral=True)

    @discord.ui.button(label="لا ❌", style=discord.ButtonStyle.red, custom_id="disagree_button")
    async def disagree(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("يجب الموافقة على الشروط لتتمكن من استخدام السيرفر.", ephemeral=True)

class RulesLaunchView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="قراءة القوانين", style=discord.ButtonStyle.gray, custom_id="read_rules_button")
    async def read_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="الشروط والأحكام - Zone Store", 
            description="""1- لا يمكن استرداد المبلغ المدفوع إلا في حال تأخير التسليم عن 24 ساعة، يتم إرجاع المبلغ كاملاً.
2- جميع المنتجات غير مشمولة في الضمان إلا في حال ذكر الضمان في وصف المنتج.
3- التعويض يكون على نفس المنتج، لا يوجد تعويض مالي.
4- أي استخدام مخالف للشروط أو استغلال خاطئ للخدمة يسقط الضمان بالكامل.
5- يتحمل العميل المسؤولية كاملة في حال تزويدنا بمعلومات غير صحيحة تؤدي إلى التأخير أو الفشل في تنفيذ الطلب.
6- التقييم شيء إجباري على العميل.

**ملاحظة:** نحتفظ بحق تعديل هذه الشروط في أي وقت دون إشعار مسبق، وتكون الشروط المحدثة سارية فور نشرها.
(تاريخ آخر تحديث: 16/6/2026)""", 
            color=discord.Color.blue()
        )
        # هنا يتم استدعاء AgreementView لإظهار الزرين معاً
        await interaction.response.send_message(embed=embed, view=AgreementView(), ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(RulesLaunchView())
    bot.add_view(AgreementView())
    print(f'تم تفعيل بوت Zone Store بنجاح!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_rules(ctx):
    embed = discord.Embed(title="مرحباً بك في Zone Store", description="اضغط على الزر أدناه لقراءة القوانين والموافقة عليها.", color=discord.Color.blue())
    # استبدل هذا الرابط برابط صورة البنر الخاص بك (يجب أن ينتهي بـ .png أو .jpg)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1516223386064523317/1516574805019590789/zone_store_banner.png")
    await ctx.send(embed=embed, view=RulesLaunchView())
import os
bot.run(os.environ['DISCORD_TOKEN'])
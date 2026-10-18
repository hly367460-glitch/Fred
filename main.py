import logging
import re
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ----------------------------------------------------
# 🔑 ដាក់ Telegram Bot Token របស់អ្នកនៅទីនេះ
# ----------------------------------------------------
TELEGRAM_BOT_TOKEN = "7628196948:AAFrvAz1LnxJSqFYph7jUmEMR5ePvbiryjc"

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------
# 📌 Function សម្រាប់ទាញយក TikTok Video ដោយគ្មាន Watermark
# ----------------------------------------------------
def get_tiktok_video(tiktok_url):
    """
    ប្រើប្រាស់ TikWm API ដើម្បីទាញយក Link វីដេអូ TikTok គ្មាន Watermark
    """
    api_url = f"https://www.tikwm.com/api/?url={tiktok_url}"
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        if data.get("code") == 0:
            video_data = data.get("data", {})
            return {
                "status": True,
                "video_url": video_data.get("play"),       # វីដេអូគ្មាន Watermark
                "audio_url": video_data.get("music"),      # ចម្រៀង MP3
                "title": video_data.get("title", "TikTok Video"),
                "author": video_data.get("author", {}).get("nickname", "Unknown"),
                "views": video_data.get("play_count", 0),
                "likes": video_data.get("digg_count", 0),
                "cover": video_data.get("cover")
            }
        else:
            return {"status": False, "message": "មិនអាចស្វែងរកវីដេអូនេះបានទេ។ សូមពិនិត្យ Link ឡើងវិញ!"}
    except Exception as e:
        logger.error(f"Error fetching TikTok video: {e}")
        return {"status": False, "message": "មានបញ្ហាបច្ចេកទេស ក្នុងការទាក់ទងទៅកាន់ API!"}

# ----------------------------------------------------
# 🤖 Telegram Bot Handlers
# ----------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ប៊ូតុង និងសារស្វាគមន៍ /start"""
    user_first_name = update.effective_user.first_name
    welcome_text = (
        f"👋 **សួស្តី {user_first_name}!**\n\n"
        "✨ **ស្វាគមន៍មកកាន់ TikTok Downloader Bot** ✨\n"
        "ខ្ញុំអាចជួយអ្នកទាញយកវីដេអូ TikTok ដោយ **គ្មាន Watermark / Logo** បានយ៉ាងរហ័ស!\n\n"
        "🔗 **របៀបប្រើប្រាស់៖**\n"
        "គ្រាន់តែផ្ញើ **Link វីដេអូ TikTok** មកកាន់ខ្ញុំជាការស្រេច។"
    )
    
    # ស្ទីលប៊ូតុងលូយៗរៀបចំជួរ
    keyboard = [
        [InlineKeyboardButton("📢 Channel ផ្លូវការ", url="https://t.me/")],
        [InlineKeyboardButton("💬 ជំនួយ & ទំនាក់ទំនង", url="https://t.me/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text, 
        parse_mode="Markdown", 
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ទទួល និងដំណើរការ Link វីដេអូ TikTok"""
    message_text = update.message.text

    # បញ្ជាក់ថាជា Link TikTok ឬអត់
    tiktok_pattern = r"https?://(www\.|vm\.|vt\.|t\.)?tiktok\.com/.*"
    if not re.search(tiktok_pattern, message_text):
        await update.message.reply_text("⚠️ **សូមផ្ញើ Link វីដេអូ TikTok ឱ្យបានត្រឹមត្រូវ!**", parse_mode="Markdown")
        return

    # ផ្ញើសារប្រាប់ User ថា Bot កំពុងដំណើរការ
    processing_msg = await update.message.reply_text("⏳ **កំពុងទាញយកវីដេអូ... សូមរង់ចាំមួយភ្លែត!**", parse_mode="Markdown")

    # ទាញយកព័ត៌មានវីដេអូ
    result = get_tiktok_video(message_text)

    if result["status"]:
        caption = (
            f"🎬 **{result['title']}**\n\n"
            f"👤 **អ្នកបង្ហោះ:** {result['author']}\n"
            f"👁 **ទស្សនា:** {result['views']:,} ដង | ❤️ **Likes:** {result['likes']:,}\n\n"
            f"⚡ **Downloaded by TikTok Bot**"
        )
        
        # ប៊ូតុងទាញយក MP3 បន្ថែម
        keyboard = [
            [InlineKeyboardButton("🎵 ទាញយកភ្លេង/MP3", url=result['audio_url'])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            # ផ្ញើវីដេអូទៅកាន់ Telegram
            await update.message.reply_video(
                video=result["video_url"],
                caption=caption,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            # លុបសារ "កំពុងទាញយក" ចោល
            await processing_msg.delete()
        except Exception as e:
            logger.error(f"Error sending video: {e}")
            await processing_msg.edit_text("❌ **មានបញ្ហាក្នុងការផ្ញើវីដេអូ។ ទំហំវីដេអូអាចធំពេក!**", parse_mode="Markdown")
    else:
        await processing_msg.edit_text(f"❌ {result['message']}")

# ----------------------------------------------------
# 🚀 Main Function
# ----------------------------------------------------
def main():
    # បង្កើត Application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # បញ្ចូល Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ចាប់ផ្តើម Run Bot
    print("🚀 TikTok Downloader Bot កំពុងដំណើរការ...")
    app.run_polling()

if __name__ == "__main__":
    main()

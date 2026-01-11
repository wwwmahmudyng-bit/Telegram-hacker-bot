import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import time
import random
import json
import os

# ================== CONFIG ==================
TOKEN = "8229280525:AAGedUjQTmUdHPWGb11JXNvnaGielOa7YLw"
ADMIN_ID = 66749223
PASSWORD = "0466"
X_LINK = "https://x.com/Mahmud_sm1"
DATA_FILE = "bot_data.json"
# ===========================================

bot = telepot.Bot(TOKEN)

# ============ LOAD / SAVE ============
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_stats = json.load(f)
else:
    user_stats = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_stats, f)

# ============ TEMP DATA ============
logged_in_users = set()
waiting_for_password = set()
last_action_time = {}

# ============ SHOP ITEMS ============
SHOP_ITEMS = {
    "VPN": 50,
    "Bruteforce Tool": 100,
    "Exploit Kit": 200
}

# ============ UI ============
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📡 WiFi Hack"), KeyboardButton(text="📘 Facebook Hack")],
            [KeyboardButton(text="🏧 ATM Hack"), KeyboardButton(text="🛒 Shop")],
            [KeyboardButton(text="🎯 Missions"), KeyboardButton(text="🧰 My Tools")],
            [KeyboardButton(text="📊 My Stats"), KeyboardButton(text="🏆 Leaderboard")],
            [KeyboardButton(text="🐦 X"), KeyboardButton(text="ℹ️ Help")]
        ],
        resize_keyboard=True
    )

# ============ GAME LOGIC ============
def get_rank(level):
    if level < 3:
        return "Noob 🐣"
    elif level < 6:
        return "Script Kiddie 🧒"
    elif level < 10:
        return "Hacker 😎"
    elif level < 15:
        return "Pro Hacker 🧠"
    else:
        return "Legend 👑"

def init_user(chat_id):
    cid = str(chat_id)
    if cid not in user_stats:
        user_stats[cid] = {
            "xp": 0,
            "level": 1,
            "coins": 0,
            "tools": [],
            "missions_done": 0,
            "username": ""
        }

def add_xp(chat_id, amount):
    cid = str(chat_id)
    init_user(chat_id)

    user_stats[cid]["xp"] += amount
    user_stats[cid]["coins"] += random.randint(5, 15)

    leveled = False
    while True:
        need = user_stats[cid]["level"] * 40
        if user_stats[cid]["xp"] >= need:
            user_stats[cid]["xp"] -= need
            user_stats[cid]["level"] += 1
            leveled = True
        else:
            break

    save_data()

    if leveled:
        rank = get_rank(user_stats[cid]["level"])
        bot.sendMessage(chat_id, f"🎉 LEVEL UP!\n⭐ Level: {user_stats[cid]['level']}\n🏆 Rank: {rank}")

# ============ HANDLER ============
def handle(msg):
    chat_id = msg['chat']['id']
    text = str(msg.get('text', '')).strip()
    cid = str(chat_id)

    # Anti-spam (2 seconds)
    now = time.time()
    if chat_id in last_action_time:
        if now - last_action_time[chat_id] < 2:
            bot.sendMessage(chat_id, "⏳ Ka yi sauri! Jira kaɗan...")
            return
    last_action_time[chat_id] = now

    init_user(chat_id)

    # ===== LOGIN =====
    if chat_id in waiting_for_password:
        if text == PASSWORD:
            logged_in_users.add(chat_id)
            waiting_for_password.remove(chat_id)
            bot.sendMessage(chat_id, "✅ Login successful! Welcome Hacker 😎", reply_markup=main_menu())
        else:
            bot.sendMessage(chat_id, "❌ Wrong password! Try again:")
        return

    # ===== START =====
    if text == "/start":
        if chat_id in logged_in_users:
            bot.sendMessage(chat_id, "😎 Ka riga ka login!", reply_markup=main_menu())
        else:
            waiting_for_password.add(chat_id)
            bot.sendMessage(chat_id, "🔐 Enter password:")
        return

    # ===== MUST LOGIN =====
    if chat_id not in logged_in_users:
        bot.sendMessage(chat_id, "🔒 Da fari ka /start ka login!")
        return

    # ===== BUTTONS =====
    if text == "📡 WiFi Hack":
        bot.sendMessage(chat_id, "📡 Scanning...\n🔓 Cracking...")
        time.sleep(1)
        if random.choice([True, True, False]):
            xp = random.randint(10, 20)
            add_xp(chat_id, xp)
            bot.sendMessage(chat_id, f"✅ Success! +{xp} XP")
        else:
            bot.sendMessage(chat_id, "❌ Failed!")

    elif text == "📘 Facebook Hack":
        bot.sendMessage(chat_id, "📘 Bruteforcing...\n⚙️ Bypassing...")
        time.sleep(1)
        if random.choice([True, False]):
            xp = random.randint(15, 30)
            add_xp(chat_id, xp)
            bot.sendMessage(chat_id, f"✅ Success! +{xp} XP")
        else:
            bot.sendMessage(chat_id, "❌ Failed!")

    elif text == "🏧 ATM Hack":
        bot.sendMessage(chat_id, "🏧 Connecting...\n💻 Injecting...")
        time.sleep(1)
        if random.choice([True, False]):
            xp = random.randint(20, 40)
            add_xp(chat_id, xp)
            bot.sendMessage(chat_id, f"💰 Success! +{xp} XP")
        else:
            bot.sendMessage(chat_id, "🚨 Alarm! Failed!")

    elif text == "🛒 Shop":
        msg = "🛒 SHOP:\n"
        for item, price in SHOP_ITEMS.items():
            msg += f"- {item} = {price} coins\n"
        msg += "\nRubuta: buy VPN / buy Bruteforce Tool"
        bot.sendMessage(chat_id, msg)

    elif text.startswith("buy "):
        item = text.replace("buy ", "").strip()
        if item in SHOP_ITEMS:
            price = SHOP_ITEMS[item]
            if user_stats[cid]["coins"] >= price:
                user_stats[cid]["coins"] -= price
                user_stats[cid]["tools"].append(item)
                save_data()
                bot.sendMessage(chat_id, f"✅ Ka sayi {item}!")
            else:
                bot.sendMessage(chat_id, "❌ Ba ka da coins isassu!")
        else:
            bot.sendMessage(chat_id, "❌ Item bai wanzu ba!")

    elif text == "🧰 My Tools":
        tools = user_stats[cid]["tools"]
        if tools:
            bot.sendMessage(chat_id, "🧰 Your Tools:\n" + "\n".join(tools))
        else:
            bot.sendMessage(chat_id, "❌ Baka da tools yanzu.")

    elif text == "🎯 Missions":
        bot.sendMessage(chat_id, "🎯 Mission:\nYi hack 3 times today.\nReward: 50 coins (manual)")

    elif text == "📊 My Stats":
        s = user_stats[cid]
        rank = get_rank(s["level"])
        bot.sendMessage(chat_id,
            f"📊 STATS:\n"
            f"🏆 Rank: {rank}\n"
            f"⭐ Level: {s['level']}\n"
            f"🧠 XP: {s['xp']}\n"
            f"🪙 Coins: {s['coins']}\n"
            f"🧰 Tools: {len(s['tools'])}"
        )

    elif text == "🏆 Leaderboard":
        sorted_users = sorted(user_stats.items(), key=lambda x: x[1]["level"], reverse=True)
        msg = "🏆 TOP PLAYERS:\n"
        i = 1
        for uid, data in sorted_users[:10]:
            msg += f"{i}. ID:{uid} | Lv {data['level']}\n"
            i += 1
        bot.sendMessage(chat_id, msg)

    elif text == "🐦 X":
        bot.sendMessage(chat_id, f"🐦 Follow me:\n{X_LINK}")

    elif text == "ℹ️ Help":
        bot.sendMessage(chat_id, "Use buttons to play 😎")

    else:
        bot.sendMessage(chat_id, f"💬 You said: {text}")

# ============ START ============
MessageLoop(bot, handle).run_as_thread()
print("🤖 Hacker Game Bot v4.0 is running...")

while True:
    time.sleep(10)

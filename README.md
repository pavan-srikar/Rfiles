# 🕵️‍♂️ The Ultimate Backdoor: Remote File Access Bot 💀

we got Remote File Access Bot here.
Whether you're looking to “audit” your own systems (or someone else) to access “your own” files remotely, this bot has got you covered. Built for macOS, Windows, and Linux, this tool works everywhere.

## 💻 What This Bot Can Do (aka, Why You Should Be Very Afraid)

With this little bot, you can:

- **List Files** (`/ls`): Peek inside any directory. Imagine being able to see all the secrets, neatly listed for your convenience. It’s like having x-ray vision but for directories.
  
- **Read Files** (`/cat <filename>`): Open and read files remotely. Because who needs privacy, right? Curiosity might kill the cat, but satisfaction brought it back.

- **Download Files** (`/get <filename>`): Snatch any file off the system. Like taking candy from a baby, only the baby is a computer, and the candy is potentially incriminating data.

- **Download Directories as ZIP** (`/get_dir_zip <directory>`): Grab entire directories in one swoop. For when you’re in a hurry and need everything—**now**.

- **Download Directories Recursively** (`/get_dir <directory>`): Download every single file in a directory, one by one. Because sometimes, patience is a virtue...and sometimes it's a strategy.

- **Show Directory Structure** (`/structure`): Visualize the entire directory structure. Mapping out your new territory has never been so easy.

- **Move Up a Directory** (`/cdx`): Like sneaking up the backstairs of a building. Up, up, and away!

- **Change Directory** (`/cd <directory>`): Navigate through directories like a ghost. Silent, unseen, and unsettling.

## 🔧 Installation Instructions

1. **Clone This Repository**: Because every hacker worth their salt has a collection of backdoors.
   ```bash
   git clone https://github.com/pavan-srikar/Rfiles.git
   ```

2. **Install Dependencies**: We use Python and the `python-telegram-bot` library. Because what’s the point of a backdoor if it’s not user-friendly?

   ```bash
   pip install python-telegram-bot
   ```

3. Create Your Telegram Bot
Open Telegram and start a chat with BotFather. If you've never heard of BotFather, think of him as the godfather of bots. He makes offers you can't refuse.

Use the command /newbot and follow the instructions to create your bot.

BotFather will give you a token, something like 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11. Keep it safe. Treat it like a password to your secret lair.

Replace the placeholder in the bot script with your token:

python
Copy code
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

4. Run the Bot as python script or create executable using pyinstaller
Execute the script on macOS, Windows, or Linux. Cross-platform infiltration has never been easier.

bash
Copy code
python remote_file_access_bot.py
Congratulations! Your bot is now running, ready to do your bidding.

5. Create an Executable with PyInstaller
Because nothing says “professional” like a standalone executable. Here’s how to do it:

Install PyInstaller: If you don't have it already, install it using pip.

bash
Copy code
pip install pyinstaller
Create the Executable: Run the following command in your terminal. It will bundle your bot script into a single executable file.

bash
Copy code
pyinstaller --onefile remote_file_access_bot.py
This command will create a dist directory with your shiny new executable inside. Now you can distribute it like the digital candy it is.


   ```

## 📚 Commands Cheat Sheet

Here’s your playbook, secret agent:

- `/start`: Introduce yourself to the bot. It's polite, and it lays out your options.
- `/ls`: List files in the current directory. Because knowing is half the battle.
- `/cat <filename>`: Read a file’s content. Knowledge is power. Use it wisely... or not.
- `/get <filename>`: Download a file. Take what you need. Leave no traces.
- `/get_dir_zip <directory>`: Compress and download entire directories. One zip file, so much potential.
- `/get_dir <directory>`: Download every file in a directory, slowly and methodically. Because some things shouldn’t be rushed.
- `/structure`: Display the entire directory structure. Know your domain.
- `/cdx`: Move up one directory. Because staying too long in one place is never a good idea.
- `/cd <directory>`: Move into the specified directory. Explore. Expand. Exfiltrate.

## ⚠️ Disclaimer

This tool is intended for *authorized* testing and administrative purposes only. Don't run this for any hacking purposes.

---

**Note**: If you get caught, remember: we know nothing, we saw nothing, and we definitely didn’t help you. 

---
![Alt text](/images/image1.png)
![Alt text](/images/image2.png)
There you have it! 
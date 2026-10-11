# Friend Zone

Telegram friendship-matching bot built with Node.js, grammY, Express, and PostgreSQL.

## Features
- Profile signup: nickname, age, interests, optional bio
- Browse profiles, Like, Skip, mutual Match notifications
- Same age bracket only: users under 18 are not matched with adults
- Report, Block, and delete profile/data
- Minimal admin report list
- Health endpoint for hosting

## Requirements
- Node.js 20+
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- PostgreSQL database
- GitHub account and a Render account for deployment

## Run locally
1. Install Node.js 20 or newer.
2. Download/extract this project.
3. Run `npm install`.
4. Copy `.env.example` to `.env`.
5. Fill in `BOT_TOKEN` and `DATABASE_URL`.
6. Set `PGSSL=true` if your PostgreSQL provider requires SSL.
7. Run `npm start`.

Never commit `.env` or share your bot token. If a token leaks, revoke it with BotFather and generate a new one.

## Create the bot
1. Open @BotFather in Telegram.
2. Send `/newbot`.
3. Follow the prompts and copy the token.
4. Put the token in the host's `BOT_TOKEN` environment variable, not in source code.

## Deploy on Render
1. Push this project to a private or public GitHub repository.
2. In Render, create a PostgreSQL database and copy its internal/external connection string as appropriate for the service.
3. Create a Web Service from the repository.
4. Build command: `npm install`
5. Start command: `npm start`
6. Add environment variables:
   - `BOT_TOKEN` = token from BotFather
   - `DATABASE_URL` = PostgreSQL connection string
   - `PGSSL` = `true` if required by your database provider
   - `ADMIN_IDS` = optional comma-separated Telegram numeric user IDs for admins
7. Deploy and check `/health` on your Render service URL.

## Get your Telegram numeric user ID
Use a reputable Telegram ID bot, or add a temporary `/myid` command yourself and remove it after use. Do not use a username as an admin ID. Only put trusted admin IDs in `ADMIN_IDS`.

## Important production notes
This is a starter implementation, not a fully audited production service:
- Registration state currently uses in-memory sessions; users may need to restart registration after a service restart. For a larger bot, use persistent session storage.
- Add rate limiting, stronger age assurance, moderation workflow, database backups, and automated tests before public launch.
- User-provided age is self-declared and is not verified.
- Usernames are public Telegram usernames. The bot does not reveal phone numbers or private Telegram IDs in profile cards.
- Consider disabling direct username display until both users explicitly consent to share contact details.
- Review privacy and child-safety requirements applicable to your audience and country before launch.

## Commands
- `/start` — start or register
- `/cancel` — cancel signup
- `/delete_me` — delete your profile
- `/admin` — list open reports for admins

## Database
Tables are created automatically on startup. Keep database credentials private and enable backups.

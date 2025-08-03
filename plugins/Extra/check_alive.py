import time, asyncio, platform, os, shutil, random
from pyrogram import Client, filters

CMD = ["/", "."]

@Client.on_message(filters.command("alive", CMD))
async def check_alive(_, message):
    await message.reply_text("**You are very lucky 🤞 I am alive ❤️ Press /start to use me**")


@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")

start_time = time.time()

def format_time(seconds):
    seconds = int(seconds)
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, sec = divmod(remainder, 60)
    if days:
        return f"{days}ᴅ : {hours:02d}ʜ : {minutes:02d}ᴍ: {sec:02d}s"
    else:
        return f"{hours:02d}ʜ : {minutes:02d}ᴍ : {sec:02d}s"

def get_size(size_kb):
    """Convert KB to a human-readable format."""
    size_bytes = int(size_kb) * 1024
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def get_system_info():
    bot_uptime = format_time(time.time() - start_time)
    os_info = f"{platform.system()}"
    try:
        with open('/proc/uptime') as f:
            system_uptime = format_time(float(f.readline().split()[0]))
    except Exception:
        system_uptime = "Unavailable"
    try:
        with open('/proc/meminfo') as f:
            meminfo = f.readlines()
        total_ram = get_size(meminfo[0].split()[1])  
        available_ram = get_size(meminfo[2].split()[1])  
        used_ram = get_size(int(meminfo[0].split()[1]) - int(meminfo[2].split()[1]))
    except Exception:
        total_ram, used_ram = "Unavailable", "Unavailable"
    try:
        total_disk, used_disk, _ = shutil.disk_usage("/")
        total_disk = get_size(total_disk // 1024)
        used_disk = get_size(used_disk // 1024)
    except Exception:
        total_disk, used_disk = "Unavailable", "Unavailable"

    system_info = (
        f"💻 **System Information**\n\n"
        f"🖥️ **OS:** {os_info}\n"
        f"⏰ **Bot Uptime:** {bot_uptime}\n"
        f"🔄 **System Uptime:** {system_uptime}\n"
        f"💾 **RAM Usage:** {used_ram} / {total_ram}\n"
        f"📁 **Disk Usage:** {used_disk} / {total_disk}\n"
    )
    return system_info

async def calculate_latency():
    start = time.time()
    await asyncio.sleep(0)  
    end = time.time()
    latency = (end - start) * 1000
    return f"{latency:.3f} ms"

@Client.on_message(filters.command("system"))
async def send_system_info(client, message):
    system_info = get_system_info()
    latency = await calculate_latency() 
    full_info = f"{system_info}\n📶 **Latency:** {latency}"
    info = await message.reply_text(full_info)
    await asyncio.sleep(60)
    await info.delete()
    await message.delete()
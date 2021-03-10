import asyncio
#import aravae.bot as aravae
import lexicore.bot as lexicore
import floppobot.flopparun as floppobot
from subprocess import Popen
import sys
import os
sys.path.insert(0,'.')

print(sys.path)

#os.system('find . -type f -name "*" -exec chmod +x {} \;')
os.system('chmod +x apngopt')
os.system('chmod +x apng2gif')

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

loop = asyncio.get_event_loop()
#loop.create_task(aravae.bot.start(aravae.token))
#loop.create_task(run("cd floppobot && node index.js"))
loop.create_task(floppobot.bot.start("ODE1MjQ0NzUyNjcxNzM1ODA5.YDpl1w.Q5AzZudrF-vcZf2z9IaSnUmjRos"))
loop.create_task(lexicore.bot.start(lexicore.token))
loop.run_forever()
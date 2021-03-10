import asyncio
#import aravae.bot as aravae
import lexicore.bot as lexicore
from subprocess import Popen

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

loop = asyncio.get_event_loop()
#loop.create_task(aravae.bot.start(aravae.token))
loop.create_task(run("cd floppobot && node index.js"))
loop.create_task(lexicore.bot.start(lexicore.token))
loop.run_forever()
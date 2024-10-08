

import asyncio
import aiosmtpd
from aiosmtpd.controller import Controller


class ExampleHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith('@example.com'):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        return '250 Message accepted for delivery'


controller = Controller(ExampleHandler(), port=1025, hostname='127.0.0.1')
# controller.start()
try:
    controller.start()
    input('SMTP server running. Press Enter to stop')
    controller.stop()
    # controller.loop.run_forever()
except KeyboardInterrupt:
    pass

const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const { environment } = require('../config');

const configuration = {
    production: {
        puppeteer: {
            headless: true,
            args: [
              '--no-sandbox',
              '--disable-setuid-sandbox',
            ],
            authStrategy: new LocalAuth(),
          },
    },
    development: {
        authStrategy: new LocalAuth(),
    }
}

const whatsapp = new Client(configuration[environment || 'production']);

whatsapp.on('qr', (qr) => {
    console.log("QR Ready")
    if (environment === 'production') {
        process.env.WHATSAPP_QR = qr;
    } else {
        // qrcode.generate(qr, { small: true });
    }
});

whatsapp.on('ready', () => {
    process.env.WHATSAPP_QR = "Client is ready";
    console.log('Client is ready');
});

const extract_numbers = (phone_number) => {
    return phone_number.replace(/[^0-9]/g, '');
}

const send_message = (phone_number, message) => {
    if (message && phone_number.length < 21) { // 21 is the max length of a phone number in whatsapp else will be a WhatsApp Group
        if (typeof message === 'string') {
            whatsapp.sendMessage(extract_numbers(phone_number) + '@c.us', message).then(() => {
                console.log(`Mensaje enviado a ${extract_numbers(phone_number)}`);
            }).catch((error) => {
                console.error(`Error al enviar el mensaje a ${extract_numbers(phone_number)}: ${error}`);
            });
        }
        else if (message.media) {
            const media = new MessageMedia('image/png', message.media, { caption: message.text });
            whatsapp.sendMessage(phone_number, media).then(() => {
                console.log(`Mensaje enviado a ${extract_numbers(phone_number)}`);
            }).catch((error) => {
                console.error(`Error al enviar el mensaje a ${extract_numbers(phone_number)}: ${error}`);
            });
        } else {
            whatsapp.sendMessage(phone_number, message.text).then(() => {
                console.log(`Mensaje enviado a ${extract_numbers(phone_number)}`);
            }).catch((error) => {
                console.error(`Error al enviar el mensaje a ${extract_numbers(phone_number)}: ${error}`);
            });
        }
    }
}

whatsapp.on('message', async (message) => {
    const user_phone_number = message.from;
    if (message.from === 'status@broadcast') return;

    if (message.body.toUpperCase() === 'WORKING?') {
        send_message(user_phone_number, 'Yes, I am working!');

    }
});

module.exports = { whatsappClient: whatsapp, send_message };
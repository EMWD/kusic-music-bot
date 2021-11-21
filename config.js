module.exports = {
    app: {
        px: '!',
        token: 'OTExNjU0MzYwMzM1OTMzNDQw.YZkiSQ.gLPJhQZRr_LtIp-BIZPF_4VfomI',
        playing: 'by me'
    },

    opt: {
        DJ: {
            enabled: false,
            roleName: 'DJ',
            commands: ['back', 'clear', 'filter', 'loop', 'pause', 'resume', 'seek', 'shuffle', 'skip', 'stop', 'volume']
        },
        maxVol: 100,
        loopMessage: false,
        discordPlayer: {
            ytdlOptions: {
                quality: 'highestaudio',
                highWaterMark: 1 << 25
            }
        }
    }
};

// 音频播放器增强功能
document.addEventListener('DOMContentLoaded', function() {
    const audioPlayers = document.querySelectorAll('audio');
    
    audioPlayers.forEach(player => {
        player.addEventListener('play', function() {
            // 暂停其他正在播放的音频
            audioPlayers.forEach(otherPlayer => {
                if (otherPlayer !== player && !otherPlayer.paused) {
                    otherPlayer.pause();
                }
            });
        });
    });
});

// 搜索模式切换处理
document.addEventListener('DOMContentLoaded', function() {
    const searchModeInputs = document.querySelectorAll('input[name="search_mode"]');
    const searchInput = document.querySelector('.search-input');
    
    searchModeInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value === 'natural') {
                searchInput.placeholder = '试试这样描述：想听一些悲伤的情歌...';
            } else {
                searchInput.placeholder = '搜索歌曲或歌手...';
            }
            // 清空搜索框
            searchInput.value = '';
        });
    });
}); 
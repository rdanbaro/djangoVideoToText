function main() {

    const audioTag = document.getElementById('reproductor')
    const downloadLinkTag = document.getElementById('download-link')

    try {

        if (audioTag) {
            audioTag.play()
                ? audioTag.play()
                : audioTag.classList.add('hidden')
        }

    } catch (e) {
        downloadLinkTag.href = audioTag.src
        downloadLinkTag.classList.remove('hidden')
    }

}

document.addEventListener('DOMContentLoaded', main)
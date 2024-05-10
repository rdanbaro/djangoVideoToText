function main() {

    const audioTag = document.getElementById('reproductor')
    const downloadLinkTag = document.getElementById('download-link')

    try {

        if (audioTag) {
            audioTag.play()
        }

    } catch (e) {
        downloadLinkTag.href = audioTag.src
        downloadLinkTag.classList.remove('hidden')
        audioTag.classList.add('hidden')

    }

}

document.addEventListener('DOMContentLoaded', main)
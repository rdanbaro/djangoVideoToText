function main() {

    // DOM Elements
    const audioTag = document.getElementById('reproductor')
    const downloadLinkTag = document.getElementById('download-link')
    const transcriptionNavBarTag = document.getElementById('nav-button-transcription')
    const resumenNavBarTag = document.getElementById('nav-button-resumen')
    const keywordsNavBarTag = document.getElementById('nav-button-keywords')

    // Event Listeners
    audioTag.addEventListener('canplay', () => {
        audioTag.classList.remove('hidden');
        downloadLinkTag.classList.add('hidden')
        audioTag.play()
    });

    transcriptionNavBarTag.addEventListener('click', (e) => handleOnclick(e))
    resumenNavBarTag.addEventListener('click', (e) => handleOnclick(e))
    keywordsNavBarTag.addEventListener('click', (e) => handleOnclick(e))

    function handleOnclick(e) {
        const previousButtonActive = document.querySelector('.active')
        const previousContentShow = document.querySelector('.content-show')
        const newContentShow = document.getElementById(`${e.target.id.split('-')[2]}`)

        console.log('previousContentShow: >>', previousContentShow)
        console.log('newContentShow: >>', newContentShow)
        previousButtonActive.classList.remove('active')
        e.target.classList.add('active')

        previousContentShow.classList.remove('content-show')
        previousContentShow.classList.add('hidden')

        newContentShow.classList.remove('hidden')
        newContentShow.classList.add('content-show')

    }

}

document.addEventListener('DOMContentLoaded', main)
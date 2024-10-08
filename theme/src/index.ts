
import style from './style.scss'
import axios from 'axios'

document.addEventListener('DOMContentLoaded', () => {
    setupAxios()
    setupNavbar()
    style.init()
})

async function setupAxios() {
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
    axios.defaults.xsrfCookieName = 'csrftoken'
}

async function setupNavbar() {
    const burger = document.querySelector('.navbar-burger')
    if(burger instanceof HTMLElement) {
        burger?.addEventListener('click', () => {
            const targetId = burger.dataset.target
            if(!targetId) return
            const target = document.getElementById(targetId)
            if(!target) return
            burger.classList.toggle('is-active')
            target.classList.toggle('is-active')
        })
    }
}

async function setupDragFileUpload(tags: string = '') {
    window.addEventListener('dragenter', (e) => {
        e.preventDefault()
        document.body.classList.add('is-dragging')
    })
    window.addEventListener('dragover', (e) => {
        e.preventDefault()
        document.body.classList.add('is-dragging')
    })
    window.addEventListener('dragleave', (e) => {
        e.preventDefault()
        document.body.classList.remove('is-dragging')
    })
    window.addEventListener('drop', (e) => {
        if(!e.dataTransfer) return false
        e.preventDefault()
        document.body.classList.remove('is-dragging')

        console.log(e.dataTransfer.types)
        const hasFile = e.dataTransfer.types.some((type) => type == 'Files')
        if(hasFile) {
            Promise.all([...e.dataTransfer.files].map(async (file: File) => {
                await axios.postForm('/glyphs/upload/', {
                    'image': file,
                    'tags': tags,
                })
            })).then(() => {
                location.reload()
            })
        }
    })
}

const _global = window as any
_global.setupDragFileUpload = setupDragFileUpload

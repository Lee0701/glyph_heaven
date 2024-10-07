
import style from './style.scss'

document.addEventListener('DOMContentLoaded', () => {
    setupNavbar()
    style.init()
})

function setupNavbar() {
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

document.addEventListener("DOMContentLoaded", () => {
    let rio = document.getElementById("botaoRio")
    console.log(rio)
    let cardRio = document.getElementById("collapseOne")
    console.log(cardRio)
    let btnCollapse = document.getElementById("collapseRio")
    rio.addEventListener('click', () => {
        if(rio.classList.contains('collapsed')){
            rio.classList.remove('collapsed');
            rio.setAttribute('aria-expanded', "true")
            cardRio.classList.remove('show')
            btnCollapse.classList.remove('bi-dash-circle-dotted')
            btnCollapse.classList.add('bi-plus-circle-dotted')
        } else {
            btnCollapse.classList.add('bi-dash-circle-dotted')
            btnCollapse.classList.remove('bi-plus-circle-dotted')
            rio.classList.add('collapsed')
            cardRio.classList.add('show')
            rio.setAttribute('aria-expanded', "false")
        }
    })
})

document.addEventListener("DOMContentLoaded", () => {
    let saoPaulo = document.getElementById("botaoSP")
    console.log(saoPaulo)
    let cardSP = document.getElementById("collapseTwo")
    console.log(cardSP)
    let btnCollapse = document.getElementById("collapseSP")
    saoPaulo.addEventListener('click', () => {
        if(saoPaulo.classList.contains('collapsed')){
            saoPaulo.classList.remove('collapsed');
            saoPaulo.setAttribute('aria-expanded', "true")
            cardSP.classList.remove('show')
            btnCollapse.classList.remove('bi-dash-circle-dotted')
            btnCollapse.classList.add('bi-plus-circle-dotted')
        } else {
            btnCollapse.classList.add('bi-dash-circle-dotted')
            btnCollapse.classList.remove('bi-plus-circle-dotted')
            saoPaulo.classList.add('collapsed')
            cardSP.classList.add('show')
            saoPaulo.setAttribute('aria-expanded', "false")
        }
    })
})

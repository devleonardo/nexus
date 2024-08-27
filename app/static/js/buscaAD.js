// Função que não permite o submit caso não tenha nada escrito no input
const campoBusca = document.getElementById("floatingInputValue");
const botaoBuscarAD = document.getElementById("buscarAD");

campoBusca.addEventListener('input', () => {
    if (campoBusca.value.trim() !== '') {
        botaoBuscarAD.removeAttribute('disabled');
    } else {
        botaoBuscarAD.setAttribute('disabled', 'disabled');
    }
});
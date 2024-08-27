// Função para levar para o inicio da página ao clicar no botão scroll up
const scrollUp = document.getElementById('upScroll');
if (scrollUp) {
    scrollUp.addEventListener('click', () => {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    });
}
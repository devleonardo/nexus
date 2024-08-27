// Adiciona um evento que será executado quando o conteúdo do DOM estiver completamente carregado
document.addEventListener('DOMContentLoaded', function () {
    // Obtém o user agent do navegador e o converte para letras minúsculas
    var userAgent = navigator.userAgent.toLowerCase();
    
    // Verifica se o navegador é Chrome (ou variantes como Chromium e Crio) e não é Edge (ou variantes)
    var isChrome = /chrome|chromium|crios/.test(userAgent) && !/edge|edgios|edga/.test(userAgent);
    
    // Verifica se o navegador é Firefox
    var isFirefox = /firefox/.test(userAgent);

    // Se for Chrome, adiciona a classe 'chrome' ao elemento body
    if (isChrome) {
      document.body.classList.add('chrome');
    // Se for Firefox, adiciona a classe 'firefox' ao elemento body
    } else if (isFirefox) {
      document.body.classList.add('firefox');
    }
});

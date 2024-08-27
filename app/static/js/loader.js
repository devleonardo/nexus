// FUNÇÃO DE LOADING
window.onload = function() {
    hideLoadingOverlay();
};

function showLoadingOverlay() {
  var loadingOverlay = document.getElementById("carregamento");
  loadingOverlay.style.display = "block";
};


function hideLoadingOverlay() {
  var loadingOverlay = document.getElementById("carregamento");
  loadingOverlay.style.display = "none";
};

document.addEventListener("DOMContentLoaded", function () {
    // Adiciona um ouvinte de eventos para cada clique em links
    document.addEventListener("click", function (event) {
      // Se o clique foi em um link, evita a navegação padrão e faz uma requisição fetch
      if (event.target.className === "dropdown-item") {
        showLoadingOverlay();
      }
    });
});

// FUNÇÃO DE LOADING PARA INCORPORAR NO BOTÃO
// ADICIONE A CLASS LOADER NO BOTAO QUE DESEJAR
const btNList = document.getElementsByClassName("carregar"); // Retorna uma lista de elementos com a classe "loader"
// Itera sobre a lista de elementos e adiciona um ouvinte de evento a cada um
for (let i = 0; i < btNList.length; i++) {
  btNList[i].addEventListener("click", () => {
    showLoadingOverlay();
  });
}
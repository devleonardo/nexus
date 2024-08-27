// MODAL PARA CONFIRMAR ALTERAÇÃO NO WALLPAPER
var alterar = document.getElementById('modalWallpaper');
var openModalBtnWall = document.getElementById('wallOpenModal');
var confirmBtnWall = document.getElementById('confirmBtnWall');
var cancelBtnWall = document.getElementById('cancelBtnWall');
var loading = document.getElementById('carregamento');

// FUNÇÃO PARA ABRIR A TELA DE LOADING
function loader() {
    loading.style.display = 'block';
}

// FUNÇÃO PARA ABRIR O MODAL
function openMWall() {
    alterar.style.display = 'block';
}

// FUNÇÃO PARA FECHAR O MODAL
function closeMWall() {
    alterar.style.display = 'none';
}

// EVENTO DE CLICK NO BOTÕES
openModalBtnWall.addEventListener('click', openMWall);
// confirmBtnWall.addEventListener('click', closeMWall, loader);
confirmBtnWall.addEventListener('click', () => {
    closeMWall();
    loader();
})
cancelBtnWall.addEventListener("click", (event) => {
    event.preventDefault(); // Evita o envio do formulário
    closeMWall();
});

// HABILITA O BOTÃO DE ENVIAR FORMULÁRIO CASO SEJA ESCOLHIDO UM ARQUIVO DO TIPO IMAGEM
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('wallImagem');
    const enviarBtn = document.getElementById('wallOpenModal');

    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            enviarBtn.removeAttribute('disabled');
        } else {
            enviarBtn.setAttribute('disabled', 'disabled');
        }
    });
});



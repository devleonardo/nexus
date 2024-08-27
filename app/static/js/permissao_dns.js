// Função para mostrar o formulário de remoção de permissão e ocultar o formulário de concessão de permissão
function mostrarRemoverForm() {
    document.getElementById("remover-form").style.display = "block";
    document.getElementById("conceder-form").style.display = "none";
}

// Função para mostrar o formulário de concessão de permissão e ocultar o formulário de remoção de permissão
function mostrarConcederForm() {
    document.getElementById("remover-form").style.display = "none";
    document.getElementById("conceder-form").style.display = "block";
}
document.addEventListener('DOMContentLoaded', function() {
    const campoBuscaMAC = document.getElementById("floatingInputValue");
    const botaoBuscarMAC = document.getElementById("buscarMAC");

    campoBuscaMAC.addEventListener('input', () => {
        let macValue = campoBuscaMAC.value.replace(/[^0-9A-F]/gi, ''); // Remove caracteres não hexadecimais
        macValue = macValue.slice(0, 12); // Limita a 12 caracteres

        campoBuscaMAC.value = macValue.toUpperCase(); // Atualiza o valor do campo com os caracteres válidos e em maiúsculas

        if (macValue.length === 12) {
            botaoBuscarMAC.removeAttribute('disabled');
        } else {
            botaoBuscarMAC.setAttribute('disabled', 'disabled');
        }
    });
});
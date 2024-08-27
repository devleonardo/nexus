const botaoCalcularIP = document.getElementById("bt-enviar");
const inputSubnet = document.querySelector(".input-subnet");
const idForm = document.getElementById("form-subnet");

botaoCalcularIP.addEventListener("click", () => {
    if(inputSubnet.value.trim() !== ""){
        idForm.submit();
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const ipInput = document.getElementById('ip');
    const cidrSelect = document.getElementById('cidr');
    const formSubnet = document.getElementById('form-subnet');

    ipInput.addEventListener('input', function () {
        if (ipInput.value.includes(':')) {
            // SE O VALOR DO INPUT INCLUI ':', INDICA ENDEREÇO IPv6
            cidrSelect.innerHTML = '';
            for (let i = 128; i >= 1; i--) {
                let option = document.createElement('option');
                option.value = i;
                option.text = `/${i}`;
                cidrSelect.appendChild(option);
            }
        } else {
            // SE NÃO, É ENDEREÇO IPv4
            cidrSelect.innerHTML = '';
            for (let i = 32; i >= 1; i--) {
                let option = document.createElement('option');
                option.value = i;
                option.text = `/${i}`;
                if (i === 24) option.selected = true; // SELECT A OPÇÃO /24 COMO PADRÃO
                cidrSelect.appendChild(option);
            }
        }
    });

    formSubnet.addEventListener('submit', function (event) {
        // EVENTO QUANDO O FORMULÁRIO É SUBMETIDO

        event.preventDefault(); // EVITA O COMPORTAMENTO PADRÃO DO FORMULÁRIO (RECARGA DA PÁGINA)
        formSubnet.submit(); // SUBMETE O FORMULÁRIO
    });
});

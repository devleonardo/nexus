document.addEventListener('DOMContentLoaded', function() {
    const dominioItems = document.querySelectorAll('.dominio-item');
    const divDominiosSelecionados = document.querySelector('.container-right .div-dominios');

    dominioItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault(); // Evita o comportamento padrão do link

            // Verifica se o domínio já está na lista de selecionados
            if (!divDominiosSelecionados.querySelector(`ul[data-dominio="${this.dataset.dominio}"]`)) {
                const novoUl = document.createElement('ul');
                novoUl.className = 'item-list';
                novoUl.setAttribute('data-dominio', this.dataset.dominio);

                const novoLi = document.createElement('li');
                const linkItem = document.createElement('a');
                linkItem.href = '#';
                linkItem.className = 'dominio-item';
                linkItem.dataset.dominio = this.dataset.dominio;
                linkItem.textContent = this.textContent;
                novoLi.appendChild(linkItem);
                novoUl.appendChild(novoLi);
                divDominiosSelecionados.appendChild(novoUl);

                // Adiciona evento de clique ao novo item para removê-lo da lista de selecionados
                linkItem.addEventListener('click', function(event) {
                    event.preventDefault();
                    this.closest('ul').remove();
                });
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById("modalBlockdns");
    const btn = document.querySelector(".botaoExecutar");
    const span = document.querySelector(".close");
    const cancelBtn = document.querySelector(".btn.btn-danger");

    btn.onclick = function() {
        modal.style.display = "block";
    }

    cancelBtn.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});

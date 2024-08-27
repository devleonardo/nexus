////////////////////////////////////////////////////////////////////
//                      RADIUS SCRIPTS HTML                       //
////////////////////////////////////////////////////////////////////
// CONVERTE O VALOR PASSADO PARA O INPUT DE FORMULARIO DE DATA PARA SER PASSADO DA FORMA CORRETA
document.addEventListener('DOMContentLoaded', function () {
    const element = document.getElementById('datepickerfinal');
    console.log('Element found:', element);

    const maskOptions = {
        mask: '0000-00-00'
    };

    const mask = IMask(element, maskOptions);
})
document.addEventListener('DOMContentLoaded', function () {
    const element = document.getElementById('datepicker');
    console.log('Element found:', element);

    const maskOptions = {
        mask: '0000-00-00'
    };

    const mask = IMask(element, maskOptions);
})

// Obter o elemento input
var inputDate = document.getElementById('data');
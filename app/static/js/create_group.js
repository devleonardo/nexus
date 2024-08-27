// document.getElementById('options-create').addEventListener('change', function () {
//     if (this.value) {
//         document.getElementById('groupNameContainer').style.display = 'block';
//         document.getElementById('openModalGp').style.display = 'block';
//     } else {
//         document.getElementById('groupNameContainer').style.display = 'none';
//         document.getElementById('openModalGp').style.display = 'none';
//     }
// });


var openModalGp = document.getElementById('openModalGp');
var modalGp = document.getElementById('modalCreateGp');
var btnSubmitGp = document.getElementById('modalCreateGp');
var createGroupForm = document.getElementById('groupForm-create');

openModalGp.addEventListener('click', function(event) {
    event.preventDefault();
    modalGp.style.display = "block";
});

btnSubmitGp.addEventListener('click', () => {
    createGroupForm.submit();
});
const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalTarget)
        //openModal(modal)
    })
})

overlay.addEventListener('click', () => {
    const modals = document.querySelectorAll('.modal.active')
    modals.forEach(modal => {
        closeModal(modal)
    })
})

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal')
        closeModal(modal)
    })
})

function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}

const calcButton = document.getElementById('calc');
const body = document.getElementById('modal-info');


calcButton.addEventListener('click', async () => {
    const sum = document.getElementById('total-sum');
    const buttons1 = document.querySelectorAll('#second .fill.active');
    if (buttons1.length == 0) return;
    var floorCount = buttons1[0].innerHTML
    const buttons2 = document.querySelectorAll('#third .fill2.active');
    if (buttons2.length == 0) return;
    
    var modal = document.querySelector(calcButton.dataset.modalTarget);
    openModal(modal);

    const designId = buttons2[0].innerHTML;
    console.log(buttons1);
    const slider = document.getElementById("myRange1");
    body.innerHTML = "Площадь дома: " + slider.value + " м²" + "<br>" +
        "Количество этажей: " + floorCount;

    const url = '/api/design/' + designId;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error('Failed to fetch design data');
    }
    const designData = await response.json();

    sum.innerHTML = "Сумма заказа: " + (designData.price + 0.25 * floorCount * designData.price + 0.01 * designData.price * slider.value) + "р.";
})


//test.addEventListener('click', )
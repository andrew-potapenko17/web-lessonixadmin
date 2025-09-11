function openModal(modalSelector) {
    const modal = document.querySelector(modalSelector);
    if (modal) {
        modal.classList.add("visible");
        console.log("Modal opened css");
    }
}  

function closeModal(modalSelector) {
    const modal = document.querySelector(modalSelector);
    if (modal) {
        modal.classList.remove("visible");
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const addBtn = document.getElementById("addstaff");
    const modal = document.querySelector(".choose-type");

    addBtn.addEventListener("click", function () {
        openModal(".choose-type");
        console.log("Modal opened");
    });

    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            closeModal(".choose-type");
        }
    });
});

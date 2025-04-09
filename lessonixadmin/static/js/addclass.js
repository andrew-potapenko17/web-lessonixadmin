function openModal(modalSelector) {
    const modal = document.querySelector(modalSelector);
    if (modal) {
      modal.classList.add("visible");
    }
  }
  
function closeModal(modalSelector) {
    const modal = document.querySelector(modalSelector);
    if (modal) {
        modal.classList.remove("visible");
    }
  }
  

document.querySelectorAll(
  ".addstudent-form, .editstudent-form, .deletestudent-form, .choosexlxs-form, .xlxssucces-form, .xlxserror-form"
).forEach((modal) => {
  modal.addEventListener("click", function (e) {
    if (e.target === modal) {
        modal.classList.remove("visible");
        }
    });
});
  
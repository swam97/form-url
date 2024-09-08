
// document.getElementById('messageForm').addEventListener('submit', function (event) {
//     event.preventDefault(); // Prevent the form from submitting the traditional way

//     let formData = new FormData(this);
//     let errorPopup = document.getElementById('error-popup');

//     fetch('/submit', {
//         method: 'POST',
//         body: formData
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.error) {
//                 errorPopup.textContent = data.error;
//                 errorPopup.style.display = 'block';
//             } else {
//                 // window.location.href = '/display?alias=' + data.short_url.split('/').pop();
//                 // console.log("here");
//                 console.log(data.short_url);
//             }
//         })
//         .catch(error => {
//             errorPopup.textContent = 'An error occurred. Please try again.';
//             errorPopup.style.display = 'block';
//         });
// });


const form = document.getElementById('messageForm');
const modal = document.getElementById('confirmationModal');
const confirmYes = document.getElementById('confirmYes');
const confirmNo = document.getElementById('confirmNo');

form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent normal form submission

    // Show the modal with form data for confirmation
    document.getElementById('confirmName').innerText = form.name.value;
    document.getElementById('confirmOccasion').innerText = form.occasion.value;
    document.getElementById('confirmMessage').innerText = form.message.value;
    document.getElementById('confirmAlias').innerText = form.custom_alias.value || 'None';

    modal.style.display = 'block'; // Show modal
});

// Handle the Yes button
confirmYes.addEventListener('click', function () {
    modal.style.display = 'none'; // Hide modal

    // Submit the form via AJAX (fetch API)
    let formData = new FormData(form);
    let errorPopup = document.getElementById('error-popup');

    fetch('/submit', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorPopup.textContent = data.error;
                errorPopup.style.display = 'block';
            } else {
                // window.location.href = '/display?alias=' + data.short_url.split('/').pop();
                console.log(data.short_url);
            }
        })
        .catch(error => {
            errorPopup.textContent = 'An error occurred. Please try again.';
            errorPopup.style.display = 'block';
        });
});

// Handle the No button (close the modal and let the user edit)
confirmNo.addEventListener('click', function () {
    modal.style.display = 'none';
});

// Close the modal when clicking outside of it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};
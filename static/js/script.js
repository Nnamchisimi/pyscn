const fileInput = document.getElementById('fileInput');
const fileLabel = document.querySelector('.file-label');
const deleteButton = document.getElementById('deleteButton');

fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        fileLabel.textContent = fileName; // Display the chosen file name
        deleteButton.disabled = false; // Enable the delete button
    } else {
        fileLabel.textContent = 'No file chosen'; // Reset the label if no file is selected
        deleteButton.disabled = true; // Disable the delete button
    }
});

function deleteFile() {
    // Confirm deletion before proceeding
    if (confirm('Are you sure you want to delete the uploaded file?')) {
        alert('File deletion logic would go here.'); // Placeholder for deletion logic
        // Add logic to remove the file on the server if necessary
    }
}

document.getElementById('uploadForm').onsubmit = async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this); // Gather form data
    alert('Form submitted!'); // Placeholder alert for form submission
    // Add logic to handle the form data (like AJAX submission) if necessary
};

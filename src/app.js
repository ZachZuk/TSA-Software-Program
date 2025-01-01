// function for going from the home page to the diagnosis page and also run the python code for diagnosing the plant
function diagnosis(plant) {
    window.location.href = "diagnosis.html";
    // create a file with info about diagnosis for other pages to use
}

function diagnose(plant) {
    window.location.href = 'diagnose.html';
}

// function for switching pages that doesn't need other stuff to be run
function goToPage(page) {
    window.location.href = page;
}

// Get the image file input element
const imageInput = document.getElementById('file-input');

// Get the dropdown element
const plantDropdown = document.getElementById('plant-dropdown');

const plantConversions = {
    'Select Plant Type': null,
    'Apple': 'Apple',
    'Cherry': 'Cherry_(including_sour)',
    'Corn': 'Corn_(maize)',
    'Grape': 'Grape',
    'Peach': 'Peach',
    'Bell Pepper': 'Pepper,_bell',
    'Potato': 'Potato',
    'Strawberry': 'Strawberry',
    'Tomato': 'Tomato'
}


const diagnoseButton = document.getElementById('diagnose-button');
console.log(diagnoseButton)
// Add an event listener to the diagnose button
diagnoseButton.addEventListener('click', async (event) => {  
  // Get the selected plant type
  const plantType = plantDropdown.options[plantDropdown.selectedIndex].text;

  // Validate plant type selection
  if (!plantConversions[plantType]) {
    alert('Please select a valid plant type');
    return;
  }

  // Get the selected image file
  const imageFile = imageInput.files[0];

  // Validate image file
  if (!imageFile) {
    alert('Please select an image');
    return;
  }

  // Create a form data object
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('plant_type', plantConversions[plantType]);

  // Send the form data to the server
  try {
    const response = await fetch('http://127.0.0.1:5000/diagnose', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    alert(data);
    alert(data.diagnosis);
  } catch (error) {
    console.error(error);
    alert(error);
  }
});
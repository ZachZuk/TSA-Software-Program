// function for going from the home page to the diagnosis page and also run the python code for diagnosing the plant
function diagnosis(diagnosisResult) {
  // Store the diagnosis result in sessionStorage
  sessionStorage.setItem('diagnosisResult', diagnosisResult);
  window.location.href = "diagnosis.html";
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
  console.log('Button clicked'); // Debug point 1
  
  const plantType = plantDropdown.options[plantDropdown.selectedIndex].text;
  console.log('Plant type:', plantType); // Debug point 2
  
  if (!plantConversions[plantType]) {
    alert('Please select a valid plant type');
    return;
  }
  
  const imageFile = imageInput.files[0];
  console.log('Image file:', imageFile); // Debug point 3
  
  if (!imageFile) {
    alert('Please select an image');
    return;
  }
  
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('plant_type', plantConversions[plantType]);
  
  console.log('FormData created with:'); // Debug point 4
  for (let [key, value] of formData.entries()) {
    console.log(key, ':', value);
  }
  
  try {
    console.log('Starting fetch...');
    const response = await fetch('http://127.0.0.1:5000/diagnose', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json'
      },
      mode: 'cors',  // Explicitly state we're making a CORS request
      credentials: 'omit'  // Don't send credentials for cross-origin requests
    });
    console.log('Fetch completed, response:', response);
    
    const data = await response.json();
    console.log('Response data:', data);
    
    if (data && data.diagnosis) {
      diagnosis(data.diagnosis);
    } else {
      alert('Invalid response format from server');
    }
    
} catch (error) {
    console.error('Detailed error:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    });
    alert(`Error: ${error.message}`);
}
});

// function for going from the home page to the diagnosis page and also run the python code for diagnosing the plant
function diagnosis(diagnosisResult) {
  // Store the diagnosis result in sessionStorage
  sessionStorage.setItem('diagnosisResult', diagnosisResult);
  window.location.href = "diagnosis";
}

function diagnose() {
    window.location.href = 'diagnose';
}

// function for switching pages that doesn't need other stuff to be run
function goToPage(page) {
    window.location.href = page;
}

// Get the image file input element
const imageInput = document.getElementById('file-input');
if (!imageInput) {
    console.error('Could not find image input element');
} else {
    console.log(imageInput);
}


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
diagnoseButton.addEventListener('click', async (event) => {  
  console.log('Button clicked');
  
  const plantType = plantDropdown.options[plantDropdown.selectedIndex].text;
  console.log('Plant type:', plantType);
  
  if (!plantConversions[plantType]) {
    alert('Please select a valid plant type');
    return;
  }
  
  const imageFile = imageInput.files[0];
  console.log('Image file:', imageFile);
  
  if (!imageFile) {
    alert('Please select an image');
    return;
  }

  showSpinner();
  
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('plant_type', plantConversions[plantType]);
  
  console.log('FormData created with:');
  for (let [key, value] of formData.entries()) {
    console.log(key, ':', value);
  }
  
  try {
    console.log('Starting fetch...');
    const response = await fetch('http://127.0.0.1:5000/diagnose_plant', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json'
      },
      mode: 'cors',
      credentials: 'omit' 
    });
    console.log('Fetch completed, response:', response);
    
    const data = await response.json();
    console.log('Response data:', data);

    hideSpinner();
    
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

function showSpinner() {
  document.getElementById('loading-spinner').style.display = 'block';
}

function hideSpinner() {
  document.getElementById('loading-spinner').style.display = 'none';
}
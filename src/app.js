// function to bring user to diagnosis page with the diagnosis result
function diagnosis(diagnosisResult) {
  // Store the diagnosis result in sessionStorage
  sessionStorage.setItem('diagnosisResult', diagnosisResult);
  window.location.href = "diagnosis";
}

// bring user to diagnose page
function diagnose() {
    window.location.href = 'diagnose';
}

// function for switching pages that don't need anything else
function goToPage(page) {
    window.location.href = page;
}

// Get the image file input element for diagnosing
const imageInput = document.getElementById('file-input');
// cheching if image was input
if (!imageInput) {
    console.error('Could not find image input element');
} else {
    console.log(imageInput);
}


// Get the plant dropdown used to select plant type
const plantDropdown = document.getElementById('plant-dropdown');

// needs this for some reason, switches things around otherwise
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

<<<<<<< Updated upstream
// Checks lots of edge cases to ensure the user is selecting the correct values

=======
// diagnose button element
>>>>>>> Stashed changes
const diagnoseButton = document.getElementById('diagnose-button');
// checking it for debugging
console.log(diagnoseButton)

// event listener to diagnose when button is clicked
diagnoseButton.addEventListener('click', async (event) => {  
  
  // getting plant type from dropdown
  const plantType = plantDropdown.options[plantDropdown.selectedIndex].text;
  
  // making sure plant selected is valid, creating alert and returning otherwise
  if (!plantConversions[plantType]) {
    alert('Please select a valid plant type');
    return;
  }
  
  // getting image from image input
  const imageFile = imageInput.files[0];
  
  // making sure the user provided an image, alerting them if not
  if (!imageFile) {
    alert('Please select an image');
    return;
  }

  // showing the spinner so users know something is going on
  showSpinner();
  
  // creating formdata to be sent to the diagnose_plant route
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('plant_type', plantConversions[plantType]);
  
  // logging formdata for debugging
  console.log('FormData created with:');
  for (let [key, value] of formData.entries()) {
    console.log(key, ':', value);
  }
  
  // using diagnose_plant route with error handling
  try {
    // fetching the route with related formdata
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
    
    // getting the response data
    const data = await response.json();
    console.log('Response data:', data);

    // hiding spinner after diagnosis is completed
    hideSpinner();
    
    // using diagnosis function to bring user to the diagnosis page with their disease, alerting them if an issue occured
    if (data && data.diagnosis) {
      diagnosis(data.diagnosis);
    } else {
      alert('Invalid response format from server');
    }
    
} catch (error) {
    // logging a detailed error to the console and alerting user with the message.
    console.error('Detailed error:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    });
    alert(`Error: ${error.message}`);
}
});

// stuff for showing and hiding spinner
function showSpinner() {
  document.getElementById('loading-spinner').style.display = 'block';
}

function hideSpinner() {
  document.getElementById('loading-spinner').style.display = 'none';
}
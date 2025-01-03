function setupFormValidation(formId, inputIds, errorIds, submitButtonId) {
  const form = document.getElementById(formId);
  const inputs = {};
  const errors = {};
  const submitButton = document.getElementById(submitButtonId);

  // Initialize inputs and errors
  for (const field in inputIds) {
      inputs[field] = document.getElementById(inputIds[field]);
      errors[field] = document.getElementById(errorIds[field]);
  }

  // Track if fields have been interacted with and if they're valid
  const touched = {};
  const valid = {};
  for (const field in inputIds) {
      touched[field] = false;
      valid[field] = false;
  }

  function validateForm() {
    // Validate First Name
    if (touched.firstName || inputs.firstName.value.trim() !== "") {
        touched.firstName = true;
        valid.firstName = /^[A-Za-z]{2,50}$/.test(inputs.firstName.value.trim());
        errors.firstName.textContent = valid.firstName ? "" : "First name must contain only letters (2-50 characters).";
    }

    // Validate Last Name
    if (touched.lastName || inputs.lastName.value.trim() !== "") {
        touched.lastName = true;
        valid.lastName = /^[A-Za-z]{2,50}$/.test(inputs.lastName.value.trim());
        errors.lastName.textContent = valid.lastName ? "" : "Last name must contain only letters (2-50 characters).";
    }

    // Validate Date of Birth
    if (touched.dob || inputs.dob.value !== "") {
        touched.dob = true;
        const dobValue = new Date(inputs.dob.value);
        const today = new Date();
        valid.dob = !isNaN(dobValue) && dobValue <= today;
        errors.dob.textContent = valid.dob ? "" : "Date of birth cannot be in the future.";
    }

    // Enable submit button only if all fields are valid and touched
    const allValid = Object.values(valid).every(Boolean);
    const allTouched = Object.values(touched).every(Boolean);
    submitButton.disabled = !(allValid && allTouched);

    // console.log("Validation state:", { touched, valid, allTouched, allValid, buttonDisabled: submitButton.disabled });
  }

  // Set up event listeners
  for (const field in inputs) {
      inputs[field].addEventListener('input', () => {
          touched[field] = true;
          validateForm();
      });
  }

  // Initial validation
  validateForm();

  return validateForm;
}
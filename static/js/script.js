document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Symptom selection animation
    const symptoms = document.querySelectorAll('.symptom-checkbox');
    symptoms.forEach(symptom => {
        symptom.addEventListener('change', function() {
            if (this.checked) {
                this.parentElement.style.backgroundColor = '#ffe6f2';
            } else {
                this.parentElement.style.backgroundColor = 'transparent';
            }
        });
    });

    // Form validation and submission handling
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('#predict-button');
            const buttonText = submitButton.querySelector('.button-text'); // Assumes button text is wrapped in a span with this class
            const spinner = submitButton.querySelector('.spinner-border');   // Assumes spinner is a class

            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Check if at least one symptom is selected
                const symptoms = form.querySelectorAll('input[name="symptoms"]:checked');
                if (symptoms.length === 0) {
                    event.preventDefault();
                    alert('Please select at least one symptom');
                    return;
                }

                // Show loading state
                if (buttonText) buttonText.textContent = 'Analyzing...'; //Handle potential null
                if (spinner) spinner.classList.remove('d-none'); //Handle potential null
                submitButton.disabled = true;
            }
            form.classList.add('was-validated');
        });
    });
});

(function() {
    'use strict'
    // Form field display logic
    var linearFields = document.getElementById('linear-fields');
    var randomFields = document.getElementById('random-fields');
    var selectGroup = document.getElementById('main-form');

    selectGroup.addEventListener('change', function(event) {
      if (event.target.value === 'linear') {
        randomFields.classList.add('d-none');
        linearFields.classList.remove('d-none');
      } 
      else if(event.target.value === 'random') {
        randomFields.classList.remove('d-none');
        linearFields.classList.add('d-none');
    }

    event.preventDefault()
    event.stopPropagation()

    });
      
})();
    

// Form validation - Generated with assistance from Perplexity AI

(function() {
      'use strict'
    
      document.getElementById('main-form').onsubmit = function(e) {
        e.preventDefault(); // Prevent the default form submission
      
        // Perform your validation logic here
        var selectValue = document.getElementById('SelectVis').value;
        
        if (selectValue == "linear") {

          var slope = document.getElementById('slope').value;
          var intercept = document.getElementById('intercept').value;

          if(slope == '' || intercept == '')
            document.getElementById('form-error').innerText = "Please fill all required fields";
            return; // Stop submission if validation fails
        }

        else if (selectValue == "random"){

          var minVal = document.getElementById('min').value;
          var maxVal = document.getElementById('max').value;

          if(minVal == '' || maxVal == '')
          {
            document.getElementById('form-error').innerText = "Please fill all required fields";
            return; // Stop submission if validation fails
          }

          if(minVal >= maxVal)
          {
            document.getElementById('form-error').innerText = "Minimum value must be smaller than Maximum value!";
            minVal.focus(); 
            return; // Stop submission if validation fails
          }
        }
      
        // If validation passes, submit the form
        this.submit(); // This will submit the form programmatically
      };
    
    })();
    
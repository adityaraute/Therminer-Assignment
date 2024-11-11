// Form field display logic
(function() {
    'use strict'
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
          {
            document.getElementById('form-error').innerText = "Please fill all required fields";
            return; // Stop submission if validation fails
          }
        }

        else if (selectValue == "random"){

          var minVal = document.getElementById('min').value;
          var maxVal = document.getElementById('max').value;

          if(minVal == '' || maxVal == '')
          {
            document.getElementById('form-error').innerText = "Please fill all required fields";
            return; // Stop submission if validation fails
          }

          if(parseFloat(minVal) >= parseFloat(maxVal))
          {
            document.getElementById('form-error').innerText = "Minimum value must be smaller than Maximum value!";
            return; // Stop submission if validation fails
          }
        }
      
        // If validation passes, submit the form
        this.submit(); // This will submit the form programmatically
      };
    
})();
  
// Hide the new graph onload 
//(Source: https://community.plotly.com/t/displaying-a-hidden-div-changes-the-layout/30072/2)
(function(){
  try{
    document.getElementById('pred_graph').classList.add("d-none");
  }
  catch(e){}
})();

// Onclick function for View More Information
function showinfo(el) {
  if(el.innerText == 'View More Information'){
    el.innerText = "Hide Below Information";
    document.getElementById('more-info-table').classList.remove("d-none");
    document.getElementById('pred_graph').classList.remove("d-none");
  }
  else{
    el.innerText = 'View More Information';
    document.getElementById('more-info-table').classList.add("d-none");
    document.getElementById('pred_graph').classList.add("d-none");
  }
}
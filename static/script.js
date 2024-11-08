(function() {
    'use strict'
  
    // var form = document.querySelector('form');
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
  
  })()
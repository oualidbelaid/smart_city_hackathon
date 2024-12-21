document.addEventListener('DOMContentLoaded', function() {
    const openModalButton = document.getElementById('openModal');
    const modal = document.getElementById('constraintModal');
    const submitConstraintButton = document.getElementById('submitConstraint');
    const timeInput = document.getElementById('timeInput');
    const budgetInput = document.getElementById('budgetInput');
    const constraintRadios = document.querySelectorAll('input[name="constraint"]');
    const messageContainer = document.getElementById('messages');
    let selectedConstraintType = null; // Variable to store the selected constraint type

    // Initialize Flatpickr
    flatpickr("#myCalendar", {
        mode: "range",
        dateFormat: "Y-m-d"
    });

    openModalButton.addEventListener('click', function() {
        modal.style.display = 'flex';
    });


    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

     constraintRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'time') {
                timeInput.style.display = 'block';
                budgetInput.style.display = 'none';
                selectedConstraintType = 'time';
            } else if (this.value === 'budget') {
                budgetInput.style.display = 'block';
                timeInput.style.display = 'none';
                 selectedConstraintType = 'budget';
            }
        });
    });

   submitConstraintButton.addEventListener('click', function() {
            let userInputValue = "";
            if (selectedConstraintType === 'time') {
                  const flatpickrInstance = document.querySelector("#myCalendar")._flatpickr;
                   userInputValue = flatpickrInstance.input.value
             } else if(selectedConstraintType === 'budget'){
                  userInputValue = document.getElementById('budgetAmount').value;

             }


           if(userInputValue) {
              sendMessage(selectedConstraintType, userInputValue);
              modal.style.display = 'none';

            }


        });
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
    });


    function sendMessage(constraintType, userValue){
         $.post("/get_suggestions/", {
                user_input: userValue,
                constraint_type: constraintType
            }, function(data) {
                 if (data.suggestions) {
                        appendMessage('bot', data.suggestions);
                    } else if (data.error) {
                        appendMessage('bot', 'Error: ' + data.error);
                    }
            });
      }

       function appendMessage(sender, text) {
            const messageDiv = document.createElement('p');
            messageDiv.classList.add(`${sender}-message`);
            messageDiv.innerHTML = text;
            messageContainer.appendChild(messageDiv);
             messageContainer.scrollTop = messageContainer.scrollHeight;
        }
});
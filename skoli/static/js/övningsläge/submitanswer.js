
//Create csrf token, copied from docs: https://docs.djangoproject.com/en/4.2/howto/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

//=================================================================================================


const submitButton = document.getElementById("submit-alternative");

submitButton.addEventListener('click', submitAnswer)

function submitAnswer(event) {
    event.preventDefault();

    const selectedChoice = document.querySelector("input[name='answer']:checked");


    if (selectedChoice) {
        // Get the value of the selected choice (choise.id)
        const submittedChoiseId = selectedChoice.value;
        console.log("Selected choice ID:", submittedChoiseId);
        // You can use this value to perform further actions, such as submitting the form.

    
    
        const url = `http://127.0.0.1:8000/api/submit-answer/${submittedChoiseId}`;
        fetch(url)
        .then(response => response.json())
        .then(data => {
            // Process the response data here
            if (data.submitted_answer == 'correct') {

                const valueToFind = `"${data.question_id}"`;

                //för att visa gröna check bilden i jump question navbar 
                const questionLink = document.querySelector(`button[type="submit"][value=${valueToFind}]`);
                questionLink.innerHTML += '<img src="/static/images/checked.png" alt="Image Description" class="jump-question-wrapper-img">'

                //för att gömma svara knappen 
                const svaraBtn = document.getElementById("submit-alternative");
                svaraBtn.style.display = 'none';

                //för att visa d gröna sucess meddelandet
                const message = document.getElementById("message");
                message.style.display = '';
                message.innerHTML = '<li class="success">Rätt, bra jobbat!</li>'



            }

            else if (data.submitted_answer == 'incorrect') {
                //för att visa d gröna sucess meddelandet
                const message = document.getElementById("message");
                message.style.display = '';
                message.innerHTML = '<li class="error">Fel svar, försök igen!</li>'
            }
          })
        .catch(error => {
        // Handle errors here
        console.error(error);
        });




    } else {
        const message = document.getElementById("message");
        message.style.display = '';
        message.innerHTML = '<li class="error">Du måste välja ett alternativ.</li>'
        console.log("No choice selected.");
    }


    
    


}

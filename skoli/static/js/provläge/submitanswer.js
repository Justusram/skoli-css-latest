
const submitButton = document.getElementById("submit-alternative");

submitButton.addEventListener('click', submitAnswer)

function submitAnswer(event) {

    const selectedChoice = document.querySelector("input[name='answer']:checked");


    if (selectedChoice) {
        // Get the value of the selected choice (choise.id)
        const submittedChoiseId = selectedChoice.value;
        console.log("Selected choice ID:", submittedChoiseId);
        // You can use this value to perform further actions, such as submitting the form.

    
    
        const url = `http://127.0.0.1:8000/api/submit-answer-provläge/${submittedChoiseId}`;
        fetch(url)
        .then(response => response.json())
        .then(data => {
            // Process the response data here


            const valueToFind = `"${data.question_id}"`;

            //för att visa gröna check bilden i jump question navbar 
            const questionLink = document.querySelector(`button[type="submit"][value=${valueToFind}]`);
            questionLink.innerHTML += '<img src="/static/images/checked.png" alt="Image Description" style="width: 25px; height: 25px; margin-left: 15px; filter: hue-rotate(100deg) saturate(100%) brightness(100%);"></img>'

            //för att gömma svara knappen 
            const svaraBtn = document.getElementById("submit-alternative");
            svaraBtn.style.display = 'none';

            //för att visa ändra knappen
            const ändraBtn = document.getElementById("change-alternative");
            ändraBtn.style.display = '';

            //för att visa d gröna sucess meddelandet
            const message = document.getElementById("message");
            message.style.display = '';
            message.innerHTML = '<li class="success-provläge">Ditt svar har registrerats</li>'


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

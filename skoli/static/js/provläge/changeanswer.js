
const changeButton = document.getElementById("change-alternative");

changeButton.addEventListener('click', changeAnswer)

function changeAnswer(event) {

    const selectedChoice = document.querySelector("input[name='answer']:checked");


    if (selectedChoice) {
        // Get the value of the selected choice (choise.id)
        const submittedChoiseId = selectedChoice.value;
        console.log("Selected choice ID:", submittedChoiseId);
        // You can use this value to perform further actions, such as submitting the form.

    
    
        const url = `http://127.0.0.1:8000/api/change-answer-provläge/${submittedChoiseId}`;
        fetch(url)
        .then(response => response.json())
        .then(data => {
            // Process the response data here
    

            //för att visa d gröna sucess meddelandet
            const message = document.getElementById("message");
            message.style.display = '';
            message.innerHTML = '<li class="success-provläge">Ditt ändring har sparats</li>'


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
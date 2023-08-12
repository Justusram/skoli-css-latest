

const questionLinks = document.getElementsByClassName("question-link");

Array.from(questionLinks).forEach((element) => {
    element.addEventListener('click', swapQuiz)
});


function swapQuiz(event) {
    const questionLinks = document.getElementsByClassName("question-link");

    for (const questionLink of questionLinks) {
        // Replace all existing classes with a new class
        questionLink.className = "question-link";
    }


    const clickedQuestion = event.currentTarget;
    clickedQuestion.className = "question-link clicked";

    const questionId = clickedQuestion.value;


    var url = `http://127.0.0.1:8000/api/question-provläge/${questionId}`;


    fetch(url)
    .then((response) => response.json())
    .then(function(data){
        console.log(data)

        //show the question
        let question = document.getElementById("question-p");
        
        if (data.question.img != null) {
            question.innerHTML = data.question.question_count + '. ' + data.question.text 
            question.innerHTML += "<br>" + "<br>" + `<img src="/static${data.question.img}"></img>`
        }
        else if (data.question.img == null) {
            question.innerHTML = data.question.question_count + '. ' + data.question.text 
        }


        //ta bort messagemeddelanden som ev visats i tidigare frågan
        const message = document.getElementById("message");
        message.style.display = 'none';
        
        //visa den clickade frågan, dess alternativ
        let choisesDiv = document.getElementById("choises")
        choisesDiv.innerHTML = ''


        for (let choise of data.choises) {
            choisesDiv.innerHTML += `
            <p> 
                <label class="quiz-alternative-button">
                        <input type="radio" name="answer" value="${choise.id}" class="quiz-alternatives" id="quiz-alternative">
                        <span class="alternative-text">
                          ${choise.header } ${choise.text}
    
                        </span>
                </label>
            </p>
            `
        }

        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        console.log('Data', data);



        //hitta rätt alternativ så att om fårgan e gjord, visas rätt alternativ som grönt elr liknande

        if (data.answered == true) {
            //för att gömma svara-knappen om användaren redan besvarat frågan
            const svaraBtn = document.getElementById("submit-alternative");
            svaraBtn.style.display = 'none';

            //för att visa ändra knappen
            const ändraBtn = document.getElementById("change-alternative");
            ändraBtn.style.display = ''

            //Hämta rätt alternativ
            const correctRadio = document.querySelector(`input[type="radio"][name="answer"][value="${data.current_choise.id}"]`);
            correctRadio.checked = true

            // const label = correctRadio.parentElement; //byt bakgrund för rätt alternativ till grön
            // label.style.backgroundColor = "#b6d3e2"




        } 
        else if (data.answered == false) {
            const svaraBtn = document.getElementById("submit-alternative");
            svaraBtn.style.display = '';

            //för att dölja ändra knappen
            const ändraBtn = document.getElementById("change-alternative");
            ändraBtn.style.display = 'none'

        }


            //Change the question-id-div to the next questions id
        questionIdDiv = document.getElementById("question-id-div");
        questionIdDiv.innerHTML = data.question.id;




        //Get question description, display the button to show it, if the question has a description
        if (data.question.question_description_img) {
            övningsBeskrivningBtn = document.getElementById("övnings-beskriving-btn");
            övningsBeskrivningBtn.style.display = 'block';
            övningsBeskrivningBtn.addEventListener('click', function(){
                //visa bilden
                questionDescription = document.getElementById("övnings-beskrivning");
                questionDescription.src = `/static${data.question.question_description_img}`
                questionDescription.style.display = 'flex';
                //visa stäng-button
                stängBtn = document.getElementById("stäng-question-description")
                stängBtn.style.display = 'flex'

                //change the background 
                homeContainer = document.querySelector(".home-container");
                homeContainer.style.backgroundColor = "rgba(0, 0, 0, 0.6)" /* Change the alpha value (0.5) to adjust the darkness */
                homeContainer.style.filter = "brightness(0.6)"
                homeContainer.style.paddingBottom = '10%'

                homeContainer2 = document.querySelector(".home-container2");
                homeContainer2.style.backgroundColor = "rgba(0, 0, 0, 0.6)" /* Change the alpha value (0.5) to adjust the darkness */
                

                //Reverse all styles when stäng is clicked
                stängBtn.addEventListener('click', function() {
                    questionDescription.style.display = 'none'

                    stängBtn.style.display = 'none'

                    homeContainer = document.querySelector(".home-container");
                    homeContainer.style.backgroundColor = "" /* Change the alpha value (0.5) to adjust the darkness */
                    homeContainer.style.filter = ""

                    homeContainer2 = document.querySelector(".home-container2");
                    homeContainer2.style.backgroundColor = ""
                })

  


            })
        }

        else {
            övningsBeskrivningBtn = document.getElementById("övnings-beskriving-btn");
            övningsBeskrivningBtn.style.display = 'none';
        }



        // Visa och gömma navigationsknappar (nästa, tbx) beroende på om första och sista fråga är sant elr inte.
        const tillbakaBtn = document.getElementById("tillbaka-btn")
        const nästaBtn = document.getElementById("nästa-btn")

        // Göm tbx btn om vi är på första frågan
        if (data.första_fråga == true) {
            tillbakaBtn.style.display = 'none';
        }
        else {
            tillbakaBtn.style.display = '';
        }

        // Göm nästa btn om vi är på sista frågan

        lämnainBtn = document.getElementById("lämna-in-btn");

        if (data.sista_fråga == true) {
            nästaBtn.style.display = 'none';

            lämnainBtn.style.display = 'flex';
            
        }
        else {
            nästaBtn.style.display = '';
            lämnainBtn.style.display = 'none';

        }
        





        //Get question description txt, display the button to show it, if the question has a description txt
        const visaTxtDescriptionBtn = document.getElementById("visa-txt-description-btn")
        const döljTxtDescriptionBtn = document.getElementById("dölj-txt-description-btn")
        const txtDescription = document.getElementById("question-description-txt")
        const txtContent = document.getElementById("txt-description-content")
        
        //if there is a description, show it
        if (data.question.question_description_txt){
            döljTxtDescriptionBtn.style.display = '';
            txtDescription.style.display = '';
            txtContent.innerHTML = data.question.question_description_txt

            döljTxtDescriptionBtn.addEventListener('click', döljTxt) //Funktionerna hittar precis under else statement
            visaTxtDescriptionBtn.addEventListener('click', visaTxt) //Funktionerna hittar precis under else statement

        }
    //if there is NO description, hide all btns related to the txt description
        else {
            txtDescription.style.display = 'none';
            visaTxtDescriptionBtn.style.display = 'none'
            döljTxtDescriptionBtn.style.display = 'none';


        }


        function visaTxt() {

            visaTxtDescriptionBtn.style.display = 'none'
            döljTxtDescriptionBtn.style.display = '';
            txtDescription.style.display = '';

        }

        function döljTxt(){
            visaTxtDescriptionBtn.style.display = ''

            döljTxtDescriptionBtn.style.display = 'none';
            txtDescription.style.display = 'none';



        }
        //________END_______######










    })


    // let question = document.getElementById("question-p");

    // question.innerHTML = data.question.question_count + ' ' + data.question.text
}


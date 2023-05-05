// get category from <script> dataset
const script_data = document.getElementById("quiz_script").dataset
const category_slug = script_data.category

// handle quiz page DOM
const quiz_category_title = document.getElementById("quiz_category_title")
const quiz_area = document.getElementById("quiz_area")
const loading_placeholder = document.getElementById("loading_placeholder")
const error_message_box = document.getElementById("error_message_box")
const timeout_message_box = document.getElementById("timeout_message_box")
const countdown_tag = document.getElementById("countdown_tag")
// quiz result page
const quiz_result = document.getElementById("quiz_result")
const quiz_result_score = document.getElementById("quiz_result_score")
const quiz_result_score_max = document.getElementById("quiz_result_score_max")

const quiz_container = document.getElementById("quiz_container")
const quiz_question = document.getElementById("quiz_question")
const quiz_difficulty = document.getElementById("quiz_difficulty")
const quiz_options = document.getElementById("quiz_options")
const quiz_opt_1 = document.getElementById("quiz_opt_1")
const quiz_opt_2 = document.getElementById("quiz_opt_2")
const quiz_opt_3 = document.getElementById("quiz_opt_3")
const quiz_opt_4 = document.getElementById("quiz_opt_4")
const btn_next_question = document.getElementById("btn_next_question")
const quiz_page_current = document.getElementById("quiz_page_current")
const quiz_page_max = document.getElementById("quiz_page_max")

// 10 questions per quiz
let questions_count = 5
let current_page = 0

// keep count of correct answers
let correct_answers_count = 0

async function fetchQuestionAnswers(category) {
    const url = `/get-question-by-category/${category}`
    try {
        const response = await fetch(url)
        const data = await response.json()
        return { data }
    } catch (error) {        
        return { error }
    }
}

async function submitAnswer(category_slug, status) {
    const url = `/submit-answer/${category_slug}/${status}`
    try {
        await fetch(url, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": csrf_token,
                "Content-Type": "application/json"
            }
        })
    } catch (error) {
        return { error }
    }
}

async function handleQuestionsAnswers(category) {
    // if at the last question, change "Next Question" to "See Done"
    if(Number(quiz_page_current.textContent) + 1 === questions_count) {
        btn_next_question.textContent = "Done"
    }

    // button at final question is cicked 
    if(current_page === questions_count) {
        btn_next_question.remove()
        handleLastQuestion()
        return
    } else {
        // set question page number
        current_page = current_page + 1
        quiz_page_max.textContent = questions_count
        quiz_page_current.textContent = current_page
    }

    // make sure that the "Next Question" button is disabled
    btn_next_question.disabled = true
    // remove the button's event listeners
    btn_next_question.removeEventListener("click", async () => handleQuestionsAnswers(category_slug))
    // make sure that the "Time's up!" message box is hidden
    timeout_message_box.hidden = true

    // whilst waiting for data, hide quiz_container and show loading bar
    quiz_container.setAttribute("hidden", "")
    loading_placeholder.removeAttribute("hidden")

    const questionAnswers = await fetchQuestionAnswers(category)
    const error = questionAnswers.error
    const data = questionAnswers.data

    // update DOM according to data
    loading_placeholder.setAttribute("hidden", "")
    if(error) {
        // show error notification box
        error_message_box.hidden = false
    } else {
        handleQuizDOM(data)
    }
}

function handleLastQuestion() {
    // hide quiz area and quiz_category_title
    quiz_category_title.hidden = true
    quiz_area.hidden = true

    // submit correct answers
    for(let i=0; i<correct_answers_count; i++) {
        handleSubmitAnswer("correct")
            .then(handleQuizResultDOM())
    }

    // submit wrong answers
    let wrong_answers = questions_count - correct_answers_count
    for(let i=0; i<wrong_answers; i++) {
        handleSubmitAnswer("incorrect")
            .then(handleQuizResultDOM())
    }

    function handleQuizResultDOM() {
        // update DOM to show user score
        quiz_result.hidden = false
        quiz_result_score.textContent = correct_answers_count
        quiz_result_score_max.textContent = questions_count
    }

    // submit answer to the backend
    async function handleSubmitAnswer(user_answer) {
        const submission = await submitAnswer(category_slug, user_answer)
        try {
            return submission
        } catch (error) {
            // show error notification box
            error_message_box.hidden = false
        }
    }
}

function handleQuizDOM(data) {
    // unhide quiz_container
    quiz_container.hidden = false

    // make sure result screen is hidden
    quiz_result.hidden = true    

    // update question
    quiz_question.textContent = data.question

    // update difficulty and its CSS class
    // remove previously added color classes
    quiz_difficulty.classList.remove("is-success", "is-warning", "is-danger")
    switch (data.difficulty) {
        case 1:
            quiz_difficulty.textContent = "Easy"
            quiz_difficulty.classList.add("is-success")
            break
        case 2:
            quiz_difficulty.textContent = "Medium"
            quiz_difficulty.classList.add("is-warning")
            break
        case 3:
            quiz_difficulty.textContent = "Hard"
            quiz_difficulty.classList.add("is-danger")
            break
        default:
            break
    }

    // shuffle answers
    const shuffled_answers = shuffleAnswers(data)
    // update the buttons' textContent and value according to the resulting array from shuffleAnswers()
    quiz_opt_1.textContent = quiz_opt_1.value = shuffled_answers[0]
    quiz_opt_2.textContent = quiz_opt_2.value = shuffled_answers[1]
    quiz_opt_3.textContent = quiz_opt_3.value = shuffled_answers[2]
    quiz_opt_4.textContent = quiz_opt_4.value = shuffled_answers[3]

    handleAnswerButtons([quiz_opt_1, quiz_opt_2, quiz_opt_3, quiz_opt_4], data)
}

function shuffleAnswers(data) {
    function getRandomInt(max) {
        return Math.floor(Math.random() * max)
    }

    // get random int to place our correct answer at
    let randomInt = getRandomInt(4)
    randomInt = randomInt + 1
    
    // array to store answers
    let answers_arr = ["", "", "", ""]
    
    // handle where to place correct & incorrect answers based on randomInt
    switch (randomInt - 1) {
        case 0:
            answers_arr[0] = data["answer"]
            answers_arr[1] = data[`opt${1}`]
            answers_arr[2] = data[`opt${2}`]
            answers_arr[3] = data[`opt${3}`]
            break
        case 1:
            answers_arr[0] = data[`opt${1}`]
            answers_arr[1] = data["answer"]
            answers_arr[2] = data[`opt${2}`]
            answers_arr[3] = data[`opt${3}`]
            break
        case 2:
            answers_arr[0] = data[`opt${1}`]
            answers_arr[1] = data[`opt${2}`]
            answers_arr[2] = data["answer"]
            answers_arr[3] = data[`opt${3}`]
            break
        case 3:
            answers_arr[0] = data[`opt${1}`]
            answers_arr[1] = data[`opt${2}`]
            answers_arr[2] = data[`opt${3}`]
            answers_arr[3] = data["answer"]
            break
    }

    return answers_arr
}

function handleAnswerButtons(button_group, data) {
    // make sure seconds left <span> is empty
    countdown_tag.textContent = "" 
    countdown_tag.hidden = true 
    // reset seconds left classes
    countdown_tag.classList.remove("is-warning", "is-danger")

    // disasble buttons after a set time
    let countdown_interval
    let seconds = 15
    let seconds_left = seconds

    function countdown() {
        // check if interval already exists
        if(!countdown_interval) {
            // unhide countdown_tag and show the starting timer
            countdown_tag.hidden = false
            countdown_tag.textContent = seconds
            countdown_interval = setInterval(updateTimerDOM, 1000)
        }
    }
    
    function updateTimerDOM() {
        // make sure countdown_tag is visible
        countdown_tag.hidden = false

        // update countdown_tag
        seconds_left = seconds_left - 1
        countdown_tag.textContent = seconds_left
        if(seconds_left <= seconds / 2) {
            // half time left
            countdown_tag.classList.add("is-warning")
        }
        if(seconds_left <= 5) {
            // 5 seconds left
            countdown_tag.classList.remove("is-warning")
            countdown_tag.classList.add("is-danger")
        }
        if(seconds_left === 0) {
            countdown_tag.textContent = "0"
        }
    }

    function stopCountdown() {
        clearInterval(countdown_interval)
        // countdown_interval variable no longer holds our interval ID
        countdown_interval = null

        // also clear our questionTimeout
        clearTimeout(questionTimeout)

        // once countdown stops, hide countdown_tag
        countdown_tag.hidden = true
    }

    let questionTimeout = setTimeout(() => {
        stopCountdown()
        handleButtonsTimeout()
        countdown_tag.textContent = "0"
    }, (seconds * 1000)) // handle countdown ends

    // start countdown
    countdown()
    
    const handleButtonClick = (event) => {
        event.stopPropagation()
        event.preventDefault()

        // stop countdown once user chooses an answer
        stopCountdown()
        // disable all buttons
        disableButtons()

        const button = event.target
        
        // disable button after click
        button.disabled = true
        // if any of the buttons are clicked, enable the "Next Question" button
        btn_next_question.disabled = false

        // check if button's value attribute is the answer
        if(button.value === data.answer) {
            // correct answer
            button.classList.remove("is-danger", "is-light")
            button.classList.add("is-success")

            // update correct_answers_count
            correct_answers_count++
        } else {
            // wrong answer
            button.classList.remove("is-success", "is-light")
            button.classList.add("is-danger")
            // highlight the correct answer
            highlightCorrectAnswer()
        }
    }
    
    button_group.forEach(button => {
        // ensure the button is enabled
        button.disabled = false

        button.classList.remove("is-success", "is-light")
        button.classList.remove("is-danger", "is-light")

        // add onclick event listener to button
        button.addEventListener("click", handleButtonClick)
    })


    function handleButtonsTimeout() {
        // when time is up, disable all buttons, highlight correct answer
        disableButtons()
        // show the "Times up!" message box
        timeout_message_box.hidden = false
        // enable the "Next Question" button
        btn_next_question.disabled = false
        // highlight the correct answer
        highlightCorrectAnswer()
    }

    function disableButtons() {
        button_group.forEach(button => {
            // after clicking, disable all buttons
            button.disabled = true
            // remove event listener after clicked
            button.removeEventListener("click", handleButtonClick)
        })
    }

    function highlightCorrectAnswer() {
        button_group.forEach(button => {
            if(button.value === data.answer) {
                button.classList.add("is-success", "is-light")
            }
        })
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // once page loads, add the first question
    handleQuestionsAnswers(category_slug)

    // set question page number
    quiz_page_max.textContent = questions_count
    quiz_page_current.textContent = current_page

    // add onclick attribute to the "Next Question" button
    btn_next_question.addEventListener("click", async () => handleQuestionsAnswers(category_slug))
})
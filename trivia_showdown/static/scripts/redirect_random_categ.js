document.addEventListener('DOMContentLoaded', () => {
    const btn_random = document.getElementById("hero_btn_random")
    const category_links = document.querySelectorAll("a[data-action='category']") 

    function getRandomInt(max) {
        return Math.floor(Math.random() * max)
    }
    
    btn_random.addEventListener("click", () => {
        // get random int to randomly choose array index
        let randomInt = getRandomInt(category_links.length)

        window.location.href = category_links[randomInt].href
    })
})
//alert("!!!") // Checking if js loaded on page
document.addEventListener("DOMContentLoaded", function(){
    const form = document.getElementById("address-form")
    const url = form.dataset.url
//    alert("Here we Are!")
    console.log(url)

//    form.onsubmit = function(){}
    form.addEventListener("submit", async function(e){
        e.preventDefault()
        const formData = new FormData(form)
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value
        try{
            const response = await fetch(url, {
                method: "POST",
                headers: {
                   'X-CSRFToken': csrfToken
                },
                body: formData,
            })
            if(!response.ok){
                throw new Error("Server Error")
            }
            const data = await response.json()
//            console.log(data)
//            alert(data)
            document.getElementById("address-response").innerText = data.message || 'Success!'
        } catch(error){
            console.error(error)
            document.getElementById("address-response").innerText = "Something went wrong"
        }
    })
})

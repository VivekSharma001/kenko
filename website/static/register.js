window.addEventListener("DOMContentLoaded",()=>{
    function preview_image(event) 
    {
        var reader = new FileReader();
        reader.onload = function()
        {
            var output = document.getElementById('preview');
            output.src = reader.result;
            output.style.display="block";
            document.getElementById("ptext").style.display="block";
        }
        reader.readAsDataURL(event.target.files[0]);
    }
    document.getElementById("pimage").addEventListener("change",()=>{
        preview_image(event);
    })
})
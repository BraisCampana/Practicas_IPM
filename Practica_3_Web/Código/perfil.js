import "./VanillaQR.min.js";

const logout = document.querySelector("#logout-button");

logout.addEventListener('click', (event) => {
    location.href = "index.html";
});

document.querySelector("#button-events").addEventListener('click', (event) =>{
    getEvents();
})

window.onload = function(){
    document.querySelector("#perfil-nombre").innerHTML = sessionStorage.getItem("name");
    document.querySelector("#perfil-nombre").setAttribute("aria-label", sessionStorage.getItem("name"));

    document.querySelector("#perfil-apellido").innerHTML = sessionStorage.getItem("surname");
    document.querySelector("#perfil-apellido").setAttribute("aria-label", sessionStorage.getItem("surname"));

    document.querySelector("#perfil-email").innerHTML = "<b>Email</b>: " + sessionStorage.getItem("email");
    document.querySelector("#perfil-email").setAttribute("aria-label", "Email: " + sessionStorage.getItem("email"));

    document.querySelector("#perfil-telefono").innerHTML = "<b>Teléfono</b>: " + sessionStorage.getItem("phone");
    document.querySelector("#perfil-telefono").setAttribute("aria-label", "Teléfono: " + sessionStorage.getItem("phone"));

    document.querySelector("#perfil-login").innerHTML = "<b>Nombre de usuario</b>: " + sessionStorage.getItem("username");
    document.querySelector("#perfil-login").setAttribute("aria-label", "Nombre de usuario: " + sessionStorage.getItem("username"));

    document.querySelector("#perfil-vacunado").innerHTML = "<b>Vacunad@</b>: " + sessionStorage.getItem("is_vaccinated");
    document.querySelector("#perfil-vacunado").setAttribute("aria-label", "Vacunad@: " + sessionStorage.getItem("is_vaccinated"));
    createQr();
    getEvents();
}

function createQr(){
    var qrcode = new VanillaQR({
        url: sessionStorage.getItem("name") + ", " + sessionStorage.getItem("surname") + ", " + sessionStorage.getItem("uuid"),
        noBorder: true,
        size: 350
    });
    document.querySelector("#perfil-qr").src= qrcode.domElement.toDataURL("image/png");
}

function getEvents(){
    var numEvents = document.querySelector("#table-rows").value;
    var limit = 5;
    var myTable = document.querySelector("#table-eventos");
    var rowCount = myTable.rows.length;
    if (numEvents.trim().length > 0 && parseInt(numEvents) > 0 && parseInt(numEvents) != limit){
        limit = numEvents;
    }
    for(var x = 1; x < rowCount; x++){
        document.querySelector("#row"+ x.toString()).remove();
    }
    rowCount = 1;
    fetch('http://localhost:8080/api/rest/user_access_log/' + sessionStorage.getItem("uuid")+"?offset=0&limit="+ limit.toString(),{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-hasura-admin-secret': 'myadminsecretkey'
        }
    }).then(response =>{
        if(response.ok){
            return response.json();
        }
    }).then(responseJSON => {
        if(responseJSON["access_log"].length === 0){
            document.querySelector("#perfil-errores").innerHTML = "Este usuario no ha visitado ningún evento";
            document.querySelector("#perfil-errores").setAttribute("aria-live", "polite");
        }else{
            var row;
            for(var i = 0; i < responseJSON["access_log"].length; i++){
                var aux = responseJSON["access_log"][i]["timestamp"].toString();
                var fecha = aux.split("T")[0].split("-")[2] + "-"+aux.split("T")[0].split("-")[1] + "-"+aux.split("T")[0].split("-")[0];
                var hora = aux.split("T")[1].split(".")[0].split("+")[0];
                row = myTable.insertRow(rowCount);
                row.insertCell(0).innerHTML = responseJSON["access_log"][i]["facility"]["name"];
                row.insertCell(1).innerHTML = fecha;
                row.insertCell(2).innerHTML = hora;
                row.className = "table";
                row.id = "row" + (i+1).toString();
            }
        }
    })
    .catch(error =>{ 
        document.querySelector("p#perfil-errores").innerHTML = "No se puede conectar con el servidor";
        document.querySelector("p#perfil-errores").setAttribute("aria-live", "polite");
    });
}
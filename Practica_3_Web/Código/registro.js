import * as lib from './auxFunctions.js';

const registroForm = document.querySelector("form#registropost");
const password = document.querySelector("#password-registro");

document.querySelector("#show-password").addEventListener('click', (event) =>{
    if(password.type === "password"){
        password.type = "text";
        document.querySelector("#show-password").value = "Ocultar";
    }else if (password.type === "text"){
        password.type = "password";
        document.querySelector("#show-password").value = "Mostrar";
    }
});

  function onlyDigits(s) {
    for (let i = s.length - 1; i >= 0; i--) {
      const d = s.charCodeAt(i);
      if (d < 48 || d > 57) return false
    }
    return true
  }

function checkPhone(){
    let phone = document.querySelector("#telefono-registro").value;
    if (phone.trim().length != 9 || !onlyDigits(phone.trim())){
        return false;
    }else{
        return true;
    }
}

document.querySelector("#telefono-registro").addEventListener('change', (event)=>{
    let validPhone = checkPhone();
    if(!validPhone){
        document.querySelector("#span-telefono").innerHTML = "Introduce un teléfono válido (9 dígitos)";
        document.querySelector("#telefono-registro").className = "invalid";
        document.querySelector("#telefono-registro").setAttribute("aria-invalid", "true");
        document.querySelector("#telefono-registro").setAttribute("aria-live", "polite");
    }else{
        document.querySelector("#span-telefono").innerHTML = "&nbsp;";
        document.querySelector("#telefono-registro").className = "valid";
        document.querySelector("#telefono-registro").setAttribute("aria-invalid", "false");
        document.querySelector("#telefono-registro").removeAttribute("aria-live");
    }
})

function onlyLetters(str){
    for (let i = str.length - 1; i >=0; i--){
        var d = str.charCodeAt(i);
        if(d < 65 || (d > 90 && d < 97) || d > 122) return false;
    }
    return true;
}

function checkNameSurname(nombre){    
    if (nombre.trim().length < 3){
        return false;
    }else if(!onlyLetters(nombre.trim())){
        return false;
    }else{
        return true;
    }
}

document.querySelector("#nombre-registro").addEventListener('change', (event) =>{
    let validName = checkNameSurname(document.querySelector("#nombre-registro").value);
    if(!validName){
        document.querySelector("#span-nombre").innerHTML = "Introduce un nombre de al menos 3 caracteres alfabéticos";
        document.querySelector("#nombre-registro").className = "invalid";
        document.querySelector("#nombre-registro").setAttribute("aria-invalid", "true");
        document.querySelector("#nombre-registro").setAttribute("aria-live", "polite");
    }else{
        document.querySelector("#span-nombre").innerHTML = "&nbsp;";
        document.querySelector("#nombre-registro").className = "valid";
        document.querySelector("#nombre-registro").setAttribute("aria-invalid", "false");
        document.querySelector("#nombre-registro").removeAttribute("aria-live");
    }
})

document.querySelector("#apellido-registro").addEventListener('change', (event) =>{
    let validSurname = checkNameSurname(document.querySelector("#apellido-registro").value);
    if(!validSurname){
        document.querySelector("#span-apellido").innerHTML = "Introduce un nombre de al menos 3 caracteres alfabéticos";
        document.querySelector("#apellido-registro").className = "invalid";
        document.querySelector("#apellido-registro").setAttribute("aria-invalid", "true");
        document.querySelector("#apellido-registro").setAttribute("aria-live", "polite");
    }else{
        document.querySelector("#span-apellido").innerHTML = "&nbsp;";
        document.querySelector("#apellido-registro").className = "valid";
        document.querySelector("#apellido-registro").setAttribute("aria-invalid", "false");
        document.querySelector("#apellido-registro").removeAttribute("aria-live");
    }
})

function checkEmail(){
    let email = document.querySelector("#email-registro").value;
    const mail_format = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return mail_format.test(String(email).toLowerCase());
}

document.querySelector("#email-registro").addEventListener('change', (event) =>{
    let validEmail = checkEmail();
    if(!validEmail){
        document.querySelector("#span-email").innerHTML = "Introduce un email con al menos 6 caracteres alfanuméricos. No puede empezar por" + 
        " signos de puntuación y debe contener @ con al menos un caracter antes";
        document.querySelector("#email-registro").className = "invalid";
        document.querySelector("#email-registro").setAttribute("aria-invalid", "true");
        document.querySelector("#email-registro").setAttribute("aria-live", "polite");
    }else{
        document.querySelector("#span-email").innerHTML = "&nbsp;";
        document.querySelector("#email-registro").className = "valid";
        document.querySelector("#email-registro").setAttribute("aria-invalid", "false");
        document.querySelector("#email-registro").removeAttribute("aria-live");
    }
})

document.querySelector("#usuario-registro").addEventListener('change', (event) =>{
    if(!lib.isEmpty(document.querySelector("#usuario-registro").value)){
        document.querySelector("#span-usuario").innerHTML = "&nbsp;";
        document.querySelector("#usuario-registro").className = "valid";
        document.querySelector("#usuario-registro").setAttribute("aria-invalid", "false");
    }
})

function checkForm(){
    var fields = ["#nombre-registro", "#apellido-registro", "#email-registro", "#telefono-registro", "#usuario-registro", "#password-registro"];
    var spanFields = ["#span-nombre", "#span-apellido", "#span-email", "#span-telefono", "#span-usuario", "#span-password"];
    var validFields = 0;
    for (var i = 0; i < 6; i++){
        if (lib.isEmpty(document.querySelector(fields[i]).value)){
            document.querySelector(spanFields[i]).innerHTML = "Este campo es obligatorio"
            document.querySelector(fields[i]).className = "invalid";
            document.querySelector(fields[i]).setAttribute("aria-invalid", "true");
            document.querySelector(fields[i]).setAttribute("aria-live", "polite");
        }else if(fields[i] === "#password-registro"){
            let validPassword = lib.checkPassword();
            if(!validPassword){
                document.querySelector("#span-password").innerHTML = "Introduce una contraseña con al menos 8 caracteres alfanuméricos y con al menos "
                + "una mayúscula y una minúscula";
                document.querySelector("#password-registro").className = "invalid";
                document.querySelector("#password-registro").setAttribute("aria-invalid", "true");
                document.querySelector("#password-registro").setAttribute("aria-live", "polite");
            }else{
                document.querySelector("#span-password").innerHTML = "&nbsp;";
                document.querySelector("#password-registro").className = "valid";
                document.querySelector("#password-registro").setAttribute("aria-invalid", "false");
                document.querySelector("#password-registro").removeAttribute("aria-live");
                ++validFields;
            }
        }else if(document.querySelector(fields[i]).className === "valid"){
            ++validFields;
        }  
    } 
    if (validFields != 6) return false; 
    else return true;
}

function getVacunado(){
    if(document.querySelector("#vacunado-registro-si").checked){
        return "true";
    }else return "false";
}

registroForm.addEventListener('submit', (event) => {
    var nombre = document.querySelector("#nombre-registro").value;
    var surname = document.querySelector("#apellido-registro").value;
    var email = document.querySelector("#email-registro").value;
    var phone = document.querySelector("#telefono-registro").value;
    var username = document.querySelector("#usuario-registro").value;
    var password = document.querySelector("#password-registro").value;
    var vacunado = getVacunado();

    if(!checkForm()){
        event.preventDefault();
    }
    else{
        var data = {
            'username': username.trim(),
            'password': password.trim(),
            'name': nombre.trim(),
            'surname': surname.trim(),
            'phone': phone.trim(),
            'email': email.trim(),
            'is_vaccinated': vacunado
        };
        fetch("http://localhost:8080/api/rest/user",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-hasura-admin-secret': 'myadminsecretkey'
            },
            body: JSON.stringify(data),
        }).then(response => {
            if(!response.ok){
                document.querySelector("#span-usuario").innerHTML = "El usuario introducido ya existe, por favor introduce un usuario diferente";
                document.querySelector("#usuario-registro").className = "invalid";
            }else{
                document.querySelector("#usuario-registro").className = "valid";
                location.replace("http://localhost:8000/index.html");
            }
        })
        .catch(error => {
            document.querySelector("p#registro-error").innerHTML = "No se puede conectar con el servidor";
        });
        event.preventDefault();
    }
});

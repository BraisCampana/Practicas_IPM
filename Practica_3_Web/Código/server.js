import * as lib from './auxFunctions.js';

const password = document.querySelector("#password-formpost");
const passwordSpan = document.querySelector("#span-password");
const userSpan = document.querySelector("#span-usuario");

var nameUser;
var surname;
var email;
var phone;
var uuid;
var vacunado;

document.querySelector("#show-password").addEventListener('click', (event) =>{
  if (password.type == "password") {
    password.type = "text";
    document.querySelector("#show-password").value = "Ocultar";
  } else {
    password.type = "password";
    document.querySelector("#show-password").value = "Mostrar"; 
  }
})

function getData(response){
  nameUser = response["name"];
  surname = response["surname"];
  email = response["email"];
  phone = response["phone"];
  uuid = response["uuid"];
  if (response["is_vaccinated"] == true)
    vacunado = "Sí";
  else vacunado = "No";
}

document.querySelector('form#formpost').addEventListener('submit', (event) => {

  var login = document.querySelector("#username-formpost").value;
  var password = document.querySelector("#password-formpost").value;

  if(lib.isEmpty(login)){
    userSpan.setAttribute("aria-live", "polite");
    userSpan.innerHTML = "Introduce un nombre de usuario";
    document.querySelector("#username-formpost").className= "invalid";
    document.querySelector("#username-formpost").setAttribute("aria-invalid", "true");
    document.querySelector("#username-formpost").setAttribute("aria-live", "polite");
    if(lib.isEmpty(password)){
      passwordSpan.setAttribute("aria-live", "polite");
      passwordSpan.innerHTML = "Introduce una contraseña";
      document.querySelector("#password-formpost").className = "invalid";
      document.querySelector("#password-formpost").setAttribute("aria-invalid", "true");
      document.querySelector("#password-formpost").setAttribute("aria-live", "polite");
    }else{
      passwordSpan.innerHTML = "&nbsp;";
      document.querySelector("#password-formpost").className = "valid";
      document.querySelector("#password-formpost").setAttribute("aria-invalid", "false");
      document.querySelector("#password-formpost").removeAttribute("aria-live");
    }
    event.preventDefault(); 
  }else{
    userSpan.innerHTML = "&nbsp;";
    document.querySelector("#username-formpost").className = "valid";
    document.querySelector("#username-formpost").setAttribute("aria-invalid", "false");
    document.querySelector("#username-formpost").removeAttribute("aria-live");
    if(!lib.isEmpty(password)){   
      passwordSpan.innerHTML = "&nbsp;";
      document.querySelector("#password-formpost").className = "valid";
      document.querySelector("#password-formpost").setAttribute("aria-invalid", "false");
      document.querySelector("#password-formpost").removeAttribute("aria-live");
    }else{
      passwordSpan.setAttribute("aria-live", "polite");
      passwordSpan.innerHTML = "Introduce una contraseña";
      document.querySelector("#password-formpost").className = "invalid";
      document.querySelector("#password-formpost").setAttribute("aria-invalid", "true");
      document.querySelector("#password-formpost").setAttribute("aria-live", "polite");
    }
    event.preventDefault();
  }

  if(userSpan.innerHTML === "&nbsp;" && passwordSpan.innerHTML === "&nbsp;"){ // si los campos no están vacíos
    var data = {
      'username': login, 
      'password': password
    };
    
    fetch("http://localhost:8080/api/rest/login",{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-hasura-admin-secret': 'myadminsecretkey'
      },
      body: JSON.stringify(data)
    })
    .then(response =>{
      document.querySelector("p#login-error").innerHTML = "&nbsp;";
      if(response.ok){
        return response.json();
      }
    }).then(responseJSON => {
      if (responseJSON["users"].length === 0){
        document.querySelector("p#login-error").innerHTML = "El usuario y la contraseña introducidos son incorrectos o el usuario no existe";
      }else{
        getData(responseJSON["users"][0]);
        sessionStorage.setItem('name', nameUser);
        sessionStorage.setItem('surname', surname);
        sessionStorage.setItem('email', email);
        sessionStorage.setItem('phone', phone);
        sessionStorage.setItem('username', login);
        sessionStorage.setItem('uuid', uuid);
        sessionStorage.setItem('is_vaccinated', vacunado);
        document.querySelector('form#formpost').submit();
     }})
    .catch(error =>{ 
        document.querySelector("p#login-error").innerHTML = "No se puede conectar con el servidor"
    });
  }

});
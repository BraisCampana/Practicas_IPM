export function isEmpty(str){
    return !str.trim().length;
}

function handleErrors(response) {
    alert(response.status);
    if (response.status == 500) {
        throw Error('No se pudo conectar con el servidor');
    }
    return response.json();
}
  
function hasLowerCase(str) {
      return str.toUpperCase() != str;
}
  
function hasCamelCase(str) {
      return str.toLowerCase() != str;
}
  
function hasNumbers(str){
      const regex = /\d/;
      return regex.test(str);
}
  
export function checkPassword(){
    let password = document.querySelector("#password-registro").value;
    if (password.trim().length < 8 || !hasLowerCase(password) || !hasCamelCase(password) || !hasNumbers(password)){
        return false;
    }else{
        return true;
    }
}
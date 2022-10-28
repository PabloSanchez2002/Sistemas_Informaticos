
function validation(){
    //var erroCode = ""
    
    if(!nameCondition()){ //Aqui falta comprobar que le nombre no este en uso todavia
        alert("El nombre no es valido o ya esta siendo usado por otro usuario")
        return (false)
    }else if (!updateComplexity()|| !samePassword()){
        alert("la contraseña no cumple las condiciones establecidas")
        return (false)
    }else if(!emailCondition()){
        alert("El correo no es correcto")
        return (false)
    }else if (!cardCondition()){
        alert("El numero de tarjeta no es correcto")
        return (false)
    }else if(!addresCondition()){
        alert("La direccion no es correcta")
        return (false)
    }else{
        return (true)
    }
}

function nameCondition(){  //Aqui falta comprobar que le nombre no este en uso todavia
    var name= document.getElementById(1).value;
    var check= document.getElementById(2);
    const specialChars = /[`!@#$%^&*()_+\-=\[\]{} ;':"\\|,.<>\/?~]/;
    
    if (specialChars.test(name) || name.length == 0){
        check.innerHTML = "La contraseña no puede contener caracteres especiales ni espacios"
        return (false)
    }else{
        check.innerHTML = ""
        return (true)
    }
}

function emailCondition(){
    var email= document.getElementById(3).value;
    var check= document.getElementById(4);
    
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
  {
    check.innerHTML = ""
    return (true)
  }
    check.innerHTML = "El correo no tiene un formato valido"
    return (false)
}


function updateComplexity(){

    var password= document.getElementById(5).value;
    var complejidad= document.getElementById(6);
    var special = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;

    if(password.length < 6){
        complejidad.innerHTML = "La contraseña debe de tener al menos 6 caracteres"
        return false
    }else{
         complejidad.innerHTML = "La contraseña es aceptable😃👍️👍️"
    
        if(/\d/.test(password)){
            complejidad.innerHTML = "La contraseña es fuerte 💪😎💪😎💪"
        }
        if(special.test(password)){
            complejidad.innerHTML = "La contraseña esta fuertísima 💪😎💪😎💪😎💪😎💪"
        } 
    return true
    }
}

function samePassword(){

    var password= document.getElementById(5).value;
    var repassword= document.getElementById(7).value;
    var samePass= document.getElementById(8);
    if (password !== repassword){
        samePass.innerHTML = "Pon la misma contraseña"
        return false
    }else{
        samePass.innerHTML = ""
        return true
    }
}

function cardCondition(){
    var card= document.getElementById(9).value;
    var check= document.getElementById(10);
    if(card.length < 16 ||card.length > 16 ){
        check.innerHTML = "El numero de tarjeta debe de ser de 16 digitos"
        return false
    }else if(/^[0-9]+$/.test(card) == false){
        check.innerHTML = "Solo puedes tener numero sen este campo"
        return false
    }else{
        check.innerHTML = ""
        return true
    }
}

function addresCondition(){
    var addres= document.getElementById(11).value;
    var check= document.getElementById(12);
    if(addres.length >50){
        check.innerHTML = "La direccion es demasiado larga"
        return false
    }else{
        check.innerHTML = ""
        return true
    }
}
document.forms[0].username.focus();

var loginBtnObj = document.getElementById("loginBtn");
//loginBtnObj.addEventListener('click', validateUser);
//loginBtnObj.addEventListener('click', submitForm())

function submitForm(){

}

function validateUser(event){
    let formObj = document.getElementById("mainForm");
    let formData = new FormData(formObj);
    let url = '/loginValidation';
    postLoginValidation(url, formData)
        .then(validationMsg => displayMsg(validationMsg))
        .catch(error => console.log(error))
}
async function postLoginValidation(url, formData){
    return fetch(url, {
        method: 'POST',
        body: formData
    })
        .then((response) => response.text());
}
function displayMsg(msg){
    let loginErrorObj = document.getElementById("loginError");
    console.log("msg::" + msg);
    if (msg == 'ok') {
        msg = '';
    }
    loginErrorObj.innerHTML = msg;
}
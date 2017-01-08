function $(e){
    return document.getElementById(e);
}

function conf(){

    var str = document.getElementById("email").value;
    var pos = str.indexOf('@');
    var pos = pos+1;
    var site = str.substring(pos);

    window.open('http://' + site);    // Открывает ссылку в новой вкладке
   //document.location.href = "http://www." + site;  // Открывает ссылку на той же влкадке
    return 0;
}
function clicked(){
    alert("norm!");
}
function musicplay(){
    var audio = new Audio();
 //   audio.src = 'kasqa.mp3'; // Указываем путь к звуку "клика"
  //  audio.autoplay = true;

}

var submit = $("submit");


var btn = $("but1");

btn.onmousedown = function (){
    this.src='sign_clicked.png';
};
btn.onmouseover = function (){
    this.src='sign_onhover.png';
};
btn.onmouseup = function (){
    this.src='sign.png';
};
btn.onmouseout = function (){
    this.src='sign.png';
};

btn = $("but2");

btn.onclick = conf;

btn.onmousedown = function (){
    this.src='reg_clicked.png';
};
btn.onmouseover = function (){
    this.src='reg_onhover.png';
};
btn.onmouseup = function (){
    this.src='reg.png';
};
btn.onmouseout = function (){
    this.src='reg.png';
};

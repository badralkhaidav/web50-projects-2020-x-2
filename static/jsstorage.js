
document.addEventListener('DOMContentLoaded', () => {

localStorage.setItem('userid3', document.getElementById("user_name").innerHTML );
let chat_name = localStorage.getItem('chatroom');
if(chat_name.length>0){

  window.location.replace("chat/"+chat_name);

};

});

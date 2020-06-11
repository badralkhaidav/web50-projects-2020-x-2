
//sidenav js end
document.addEventListener('DOMContentLoaded', () => {


      // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    document.getElementById("user_name").innerHTML = localStorage.getItem('userid3');

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {

                let message = document.querySelector("#chatmessage").value;
                //let loginname = "Badral Wealthy";
                let loginname = localStorage.getItem('userid3');
                let chat_name = document.getElementById("chat_name").innerHTML;
                //let loginname = document.getElementById("loginname").innerHTML;

              //  document.querySelector('#user_name').value = loginname;
                const selection = button.dataset.vote;
                document.getElementById("chatmessage").value = "";


                socket.emit('submit chat', {'selection': selection, 'message': message, 'loginname': loginname, 'chat_name':chat_name});
            };
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('announce vote', data => {
          var timestamp = data.timestamp;
        // data.chatlist.length; //data.chatlist.lenght;

          li = document.createElement('li');
          li.innerHTML = `${data.loginname}:  ${data.message} - `+ timestamp ;
          document.querySelector('#chat').prepend(li);


    });
});

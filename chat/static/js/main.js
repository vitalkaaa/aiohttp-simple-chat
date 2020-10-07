$(function() {
    var socket = new WebSocket("ws://0.0.0.0:8080/ws");
    console.log(socket)

    socket.onopen = function() {
        console.log("Соединение установлено.");
        socket.send(JSON.stringify({
            action: 'login',
            username: $('#login').val()
        }))
    };

    socket.onclose = function(event) {
        if (event.wasClean) {
            console.log('Соединение закрыто чисто');
        } else {
            console.log('Обрыв соединения');
        }
        console.log('Код: ' + event.code + ' причина: ' + event.reason);
    };

    socket.onmessage = function(event) {
        data = JSON.parse(event.data)
        console.log(data)
        switch(data['action']) {
            case 'userlist':
                updateUserList(data['usernames']);
                break;

            case 'message':
                updateMessages(data['username'], data['text'])
                break;
        }
        console.log("Получены данные " + event.data);
    };

    socket.onerror = function(error) {
        console.log("Ошибка " + error.message);
    };


    $('#message-button').click(function(){
        socket.send(JSON.stringify({
            action: 'message',
            username: $('#login').val(),
            text: $('#message-text').val()
        }))
        $('#message-text').val('')
    })

    updateUserList = function(usernames){
        $('#user-list').empty()
        for(var i=0; i<usernames.length; i++) {
            $('#user-list').append('<p>' + usernames[i] + '</p>')
        }
    }

    updateMessages = function(username, text) {
        $('#messages').append('<p><b>' + username + ':</b> ' + text + '</p>')
    }
})
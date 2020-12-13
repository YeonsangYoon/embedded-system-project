$(document).ready(function(){
    var canvas = document.getElementById('photo_frame')
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/mynamespace");
    var msg_div = $('#message_content');
    var can_div = $('#current_can');
    var pet_div = $('#current_pet');
    var ctx;
    var canpetLock = true;


    socket.on('response', function(msg){
        
        if(msg.head === 'msg_ready'){
            msg_div.html(msg.data.replaceAll('\n','<br>'));
        }

        else if(msg.head === 'count_ready'){
            can_div.html(msg.data.can);
            pet_div.html(msg.data.pet);
        }

        else if(msg.head === 'img_ready'){
            msg_div.html('');
            ctx = canvas.getContext('2d');
            let img = new Image();
            console.log(msg.data)
            img.src = 'data:image/jpg;base64,'+msg.data
            img.onload = function(){
                ctx.clearRect(0,0,canvas.width,canvas.height);
                ctx.drawImage(img,0,0,canvas.width,canvas.height);
            }
        }

        else if(msg.head === 'button'){
            if (msg.data === 'start') {
                $('#start_button').show();
                $('#end_button').hide();
            }
            else if (msg.data === 'end') {
                $('#start_button').hide();
                $('#end_button').show();
            }
        }

        else if(msg.head === 'trigger'){
            if(msg.data === 'forceContinue'){
                $('#force_yes_button').show();
                $('#force_no_button').show();
            }
            else if(msg.data === 'endCamera'){
                ctx.clearRect(0,0,canvas.width,canvas.height);
            }
            else if(msg.data === 'showButton'){
                $('#end_button').removeClass('pressed');
                canpetLock = false;
                $('#pet_button').show();
                $('#can_button').show();
            }
        }

        else if(msg.head === 'end'){
            msg_div.html(`캔 ${msg.can}개<br>페트 ${msg.pet}개<br>총 ${msg.can+msg.pet}개 수거했습니다.`);
            can_div.html('0');
            pet_div.html('0');
        }

        else if(msg.head === 'error'){
            msg_div.html(msg.data);
        }
    });


    $('#pet_button').on('click', function(){
        if(!canpetLock){
            socket.emit('request', {'head':'button','data': 'pet'});
            $('#can_button').hide();
            canpetLock = true;
        }
    });

    $('#can_button').on('click', function(){
        if(!canpetLock){
            socket.emit('request', {'head':'button','data': 'can'});
            $('#pet_button').hide();
            canpetLock = true;
        }
    });

    $('#start_button').on('click', function(){
        $('#start_button').hide();
        $('#end_button').show();
        socket.emit('request', {'head':'button','data': 'start'});
    });

    $('#end_button').on('click', function(){
        socket.emit('request', {'head':'button','data': 'end'});
        $('#end_button').addClass('pressed');
    });

    $('#force_yes_button').on('click', function(){
        socket.emit('request', {'head':'button','data': 'force_continue','arg':'yes'})
        $('#force_yes_button').hide();
        $('#force_no_button').hide();
    });

    $('#force_no_button').on('click', function(){
        socket.emit('request', {'head':'button','data': 'force_continue','arg':'no'});
        $('#force_yes_button').hide();
        $('#force_no_button').hide();
    });

    $("form#broadcast").submit(function(event){
        if($("#input-data").val() == "")
        {
            return false;
        }
        socket.emit("request", {data: $("#input-data").val()});
        $("#input-data").val("");
        return false;
    });
});





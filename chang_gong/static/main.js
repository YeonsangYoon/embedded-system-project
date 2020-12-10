$(document).ready(function(){
    var canvas = document.getElementById('photo_frame')
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/mynamespace");
    var msg_div = $('#message_content');
    var can_div = $('#current_can');
    var pet_div = $('#current_pet');
    var ctx;


    socket.on('response', function(msg){
        
        if(msg.head === 'msg_ready'){
            msg_div.text(msg.data);
        }

        else if(msg.head === 'count_ready'){
            can_div.text(msg.data.can);
            pet_div.text(msg.data.pet);
        }

        else if(msg.head === 'img_ready'){
            ctx = canvas.getContext('2d');
            let img = new Image();
            img.src = msg.data
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
                $('#pet_button').show();
                $('#can_button').show();
            }
        }

        else if(msg.head === 'end'){
            msg_div.text(`캔 ${msg.can}개, 페트 ${msg.pet}개`);
            can_div.text('0');
            pet_div.text('0');
        }

        else if(msg.head === 'error'){
            msg_div.text(msg.data);
        }
    });


    $('#pet_button').on('click', function(){
        socket.emit('request', {'head':'button','data': 'pet'});
        $('#can_button').hide();
        
    });

    $('#can_button').on('click', function(){
        socket.emit('request', {'head':'button','data': 'can'});
        $('#pet_button').hide();
    });

    $('#start_button').on('click', function(){
        $('#start_button').hide();
        $('#end_button').show();
        socket.emit('request', {'head':'button','data': 'start'});
    });

    $('#end_button').on('click', function(){
        socket.emit('request', {'head':'button','data': 'end'});
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
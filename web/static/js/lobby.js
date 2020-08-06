function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function get_question(){
    console.log("Dificil es preguntar");
    $.getJSON("/random_question", function (data) {
        console.log(data);
        //var answers=[data.question.right_answer];
        var answers = [];
        $("#cabecera").empty();
        var div='<div id="question_desc" attr-id="question_id" class="badge badge-light"><h2>question_content</h2></div>'
        div = div.replace('question_id', data.question.id);
        div = div.replace('question_content', data.question.content); //.replace(esto, en esto)
        $("#cabecera").append(div);
        $("#options").empty();
        if (data.wrong_answers.length>0){
            $("#answer").hide();
            //combinando rpta correcta con rptas incorrectas
            var rand_int = getRandomInt(0, data.wrong_answers.length + 1);
            var it=0;
            for(let i=0; i<data.wrong_answers.length + 1; i++){
                if (i == rand_int) {
                    answers.push(data.question.right_answer);
                    console.log(i);
                    console.log(data.question.right_answer);
                } else {
                    answers.push(data.wrong_answers[it++].content);
                }
            }
            console.log(answers);
            for(var i=0; i<answers.length; i++){
                var div='<input type="radio" name="answer" id="answer'+i+'" value="answer_id">'+
                        '<label for="answer'+i+'">answer_content</label><br>';
                div = div.replace('answer_id', answers[i]);
                div = div.replace('answer_content', answers[i]); //.replace(esto, en esto)
                $("#options").append(div);
            }
        }
        else{
            $("#answer").show();
        }
        init_time(data.time);

    })
    console.log("g")
    $.getJSON("/current", function (data) {
        console.log("data:");
        console.log(data);
        let p1 = '<div><br>name is <br> a name of <br> winners</div>';
        let p2 = '<div><br>name <br> makes posible <br> the imposible</div>';
        p1 = p1.replace('name', data['name']);
        p2 = p2.replace('name', data['name']);

        $('#t-right').append(p1);
        $('#t-left').append(p2);
    })
}

function validate(){
    var selected_answer;
    if($.trim($("#options").html())==''){
        selected_answer = $('#answer').val();
    }else{
        var radios = document.getElementsByName('answer');
        for (var i = 0, length = radios.length; i < length; i++) {
            if (radios[i].checked) {
            // do whatever you want with the checked radio
                selected_answer=radios[i].value;// accedo al valor línea 7
            // only one radio can be logically checked, don't check the rest
            break;
            }
        }
    }
    var question_id=$('#question_desc').attr('attr-id');
    var ans_msg = {'answer':selected_answer, 'question_id':question_id};
    console.log(ans_msg);
    $.post({
      url:'/validate',
      type: 'post',
      dataType: 'json',
      contentType: 'application/json',
      success: function(data){
          console.log(data);
          // location.href="http://127.0.0.1:8080/static/html/lobby.html"; //redirecciono a preguntas
          if(data['msg']==="Success"){
              location.href="success.html";
          }else{
              location.href="failure.html";
          }
      },
      data: JSON.stringify(ans_msg)
    });
}
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            location.href="failure.html";
        }
    }, 1000);
}
function init_time(t_seconds) {
    var fiveMinutes = t_seconds,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};
function logout(){
  $.post({
      url:'/deauthenticate',
      type: 'post',
      dataType: 'json',
      contentType: 'application/json',
      success: function(data){
          alert(data['msg']);
          location.href="/";
      },
  });
}


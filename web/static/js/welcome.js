function get_difficulties(){
    console.log("Dificil es vivir");
    $.getJSON("/difficulties", function (data) {
        $("#difficulties").empty();
        console.log(data);
        for(var i=0; i<data.length; i++){
            console.log("hola");
            var div='<input type="radio" name="difficulty" id="difficulty'+
                    i+'" value="difficulty_id">'+
                    '<label for="difficulty'+i+'"><pre> </pre>difficulty_name</label><br>';
            div = div.replace('difficulty_id', data[i]['id']);
            //.replace(esto, en esto)
            div = div.replace('difficulty_name', data[i]['difficulty']);
            $("#difficulties").append(div);
        }
    })
}

function set_difficulty(){
    var radios = document.getElementsByName('difficulty');
    var selected_diff;
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
        // do whatever you want with the checked radio
            selected_diff=radios[i].value; // accedo al valor línea 7
        // only one radio can be logically checked, don't check the rest
        break;
        }
    }
    var diff_msg = {'difficulty_value':selected_diff};
    console.log(diff_msg);
    $.post({
      url:'/set_difficulty',
      type: 'post',
      dataType: 'json',
      contentType: 'application/json',
      success: function(data){
          console.log("Set!");
          location.href="lobby.html"; //redirecciono a preguntas
      },
      data: JSON.stringify(diff_msg)
    });
}

function start() {
    set_difficulty(); // set difficulty, ir a pregunta
}
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

function current_name() {
    getJSON("/")
}

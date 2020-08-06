function get_score(){
    console.log("Dificil es vivir part2");
    $.getJSON("/user_score", function (data) {
        console.log(data);
        $("#score").html(data['user_score']);
    })
}
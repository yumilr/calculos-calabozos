function login(){
    console.log("Login User");
    var username = $('#username').val();  //getting username by ID
    var password = $('#password').val();  // getting password by id

    var credentials = {'username':username, 'password':password};
    $.post({
        url:'/authenticate',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function(data){
            console.log("Authenticated!");
            // alert(data['msg']);
            location.href="welcome.html";
        },
        data: JSON.stringify(credentials)
    });
}

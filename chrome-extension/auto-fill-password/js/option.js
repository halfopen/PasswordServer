$(document).ready(function(){
    if(localStorage.getItem("server_address") == null){
        localStorage.setItem("server_address", "http://192.168.1.222:8000")
    }
    var new_address;
    $("input#server-address").val(localStorage.getItem("server_address"));
    $("#admin_url").attr("href", localStorage.getItem("server_address")+"/admin");

    $("#btn_update_server_address").on("click", function(){
        new_address = $("input#server-address").val();
        localStorage.setItem("server_address", new_address);
        alert("ok");
    });
});
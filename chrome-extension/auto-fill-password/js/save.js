$(document).ready(function(){

    function get_info(info){

        localStorage.setItem("url", info.url);
        $.ajax({
        type:"GET",
        url:localStorage.getItem("server_address")+"/query_website/",
        data:{"website":info.url},
        datatype: "text",//"xml", "html", "script", "json", "jsonp", "text".
        success:function(data){
             if( data=="False"){alert("False");return false;} //如果记录中没有这个网站
            localStorage.website_info = JSON.stringify(data);
            //alert(JSON.stringify(data));
        },
        error: function(){

        }});
    }

    // 点击保存密码
    function get_user_info(info){
        $("#save_password").css("display","none");
        $.ajax({
        type:"GET",
        url:localStorage.getItem("server_address")+"/save/",
        data:{"website":localStorage.url, "username":info.username, "password":info.password},
        datatype: "json",//"xml", "html", "script", "json", "jsonp", "text".
        success:function(data){
            if(data=="False"){
                $(".info").html("信息:保存失败！");
            }else if(data=="True"){
                $(".info").html("信息:保存成功！");
            }else{
                $(".info").html("信息:发生错误！");
            }
             $("#save_password").css("display","block");
        },
        error: function(){
            $(".info").html("信息:发生错误！");
            $("#save_password").css("display","block");
        }});
    }

	$("#save_password").on("click", function(){
          chrome.tabs.query({
            active: true,
            currentWindow: true
          }, function (tabs) {
            // ...and send a request for the DOM info...
            chrome.tabs.sendMessage(
                tabs[0].id,
                {from: 'save', subject: 'get_user_info', website_info:localStorage.website_info},
                get_user_info);
         });
    })


    window.addEventListener('DOMContentLoaded', function () {
	  // ...query for the active tab...
	  chrome.tabs.query({
		active: true,
		currentWindow: true
	  }, function (tabs) {
		// ...and send a request for the DOM info...
		chrome.tabs.sendMessage(
			tabs[0].id,
			{from: 'popup', subject: 'DOMInfo'},
			get_info);
	 });
	 //alert("sent");
	});
});
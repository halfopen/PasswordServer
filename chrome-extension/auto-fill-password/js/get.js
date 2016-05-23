$(document).ready(function(){
	
	function get_info(info){
        var website_info,passwords,password_html,website_html;
		//alert(info);
		$("#url").val(info.url);
        var website = $("#url").val();
		//(website);
		$.ajax({
        type:"GET",
        url:localStorage.getItem("server_address")+"/get/",
        data:{"website":website},
        datatype: "text",//"xml", "html", "script", "json", "jsonp", "text".
        success:function(data){
             if( data=="False"){alert("False");return false;}
            console.log(data);
			website_info = data.website;
			passwords = data.passwords;
			password_html = "username"+passwords[0].username+"<br/>"+"password"+passwords[0].password;
			website_html = "url"+website_info.url+"<br/>"+"username_id"+website_info.username_html_id+"<br/>"+
			"password_id"+website_info.password_html_id;
			$("#website-info").html(website_html);
			$("#password-list").html(password_html);
            // 用html5存储
            localStorage.website_info = JSON.stringify(website_info);
            localStorage.password = JSON.stringify(passwords[0]);

        },
        error: function(){

        }});
	};
	
	function fillpassword(info){}
	
	// Once the DOM is ready...
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

    /*
        自动填充密码
     */
	$("#btn-fillpassword").on('click', function () {
	  //alert("sent");
	  chrome.tabs.query({
		active: true,
		currentWindow: true
	  }, function (tabs) {
		// ...and send a request for the DOM info...
		chrome.tabs.sendMessage(
			tabs[0].id,
			{from: 'get', subject: 'fillpassword', website_info:localStorage.website_info, password:localStorage.password},
			fillpassword);
	 });
	 //alert("sent");
	}); 

    /*
        再次发送请求
    */
	$("#btn_send_request").on("click", function(){
		var website = $("#url").val();
		//(website);
		$.ajax({
        type:"GET",
        url:localStorage.getItem("server_address")+"/get/",
        data:{"website":website},
        datatype: "text",//"xml", "html", "script", "json", "jsonp", "text".
        success:function(data){
            if( data=="False"){alert("False");return false;}
            console.log(data);
			website_info = data.website;
			passwords = data.passwords;
			password_html = "username"+passwords[0].username+"<br/>"+"password"+passwords[0].password;
			website_html = "url"+website_info.url+"<br/>"+"username_id"+website_info.username_html_id+"<br/>"+
			"password_id"+website_info.password_html_id;
			$("#website-info").html(website_html);
			$("#password-list").html(password_html);
		
        },
        error: function(){

        }
    });
	});
});
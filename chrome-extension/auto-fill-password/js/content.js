var title = document.title;
var url = window.location.host;
var info = {"title":title, "url":url};
console.log(info);
// Listen for messages from the popup
chrome.runtime.onMessage.addListener(function (msg, sender, response) {
	
	console.log(msg);
	if ((msg.from === 'popup') && (msg.subject === 'DOMInfo')) {
		response(info);
		console.log("sent back");
	}else if ((msg.from == 'get') && (msg.subject == 'fillpassword')) {

		console.log(msg.website_info);
        console.log(msg.password);
        website_info = JSON.parse(msg.website_info);
        password = JSON.parse(msg.password);
        console.log(website_info);
        console.log(password);
		console.log("fillpassword");
        $(website_info.username_html_id).val(password.username);
        $(website_info.password_html_id).val(password.password);
        response("ok");
	}else if((msg.from == 'save') && (msg.subject == 'get_user_info')){
        console.log(msg.website_info);
        website_info = JSON.parse(msg.website_info);
        username = $(website_info.username_html_id).val()
        password = $(website_info.password_html_id).val();
        return_val = {username:username, password:password};
        console.log(return_val);
        response(return_val);
    }else{
		console.log("no match");
	}
});
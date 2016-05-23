/**
 * Created by Administrator on 2016/5/8.
 */
if(window.localStorage){
		console.log('你的浏览器支持localStorage!');
}else{
		console.log('浏览器不支持localStorage!');
};
if(localStorage.getItem("server_address") == null){
        localStorage.setItem("server_address", "http://192.168.1.222:8000")
}
(function(){var K='opc_cookie_choice',c=null,b=document.getElementById('cookie');try{c=localStorage.getItem(K)}catch(e){}
function ap(v){gtag('consent','update',{ad_storage:v,analytics_storage:v,ad_user_data:v,ad_personalization:v})}
function sv(v){try{localStorage.setItem(K,v)}catch(e){}ap(v);b.hidden=true}
if(c==='granted'||c==='denied')ap(c);else b.hidden=false;
document.getElementById('cookie-accept').onclick=function(){sv('granted')};
document.getElementById('cookie-decline').onclick=function(){sv('denied')};
document.getElementById('cookie-settings').onclick=function(){b.hidden=false};})();

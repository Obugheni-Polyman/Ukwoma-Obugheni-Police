(function(){
// Paste a Selar or Paystack product link between the quotes. Empty = the button orders on WhatsApp.
var LINKS={thesis:'',thesisread:'',toolkit:'https://paystack.shop/pay/iep-toolkit',goals:'https://paystack.shop/pay/iep-goals-ebook',handbook:'https://paystack.shop/pay/5opagi-y6a',faith:'https://selar.com/04967y420v',premium:'',cv:'',branding:'',templates:'https://selar.com/1n19150q5n',bizdocs:'https://selar.com/180l819186',web1:'https://paystack.com/buy/opc-basic-website--1-page-uxkqsq',web2:'https://paystack.com/buy/opc-standard-website--4-pages-puzwfs',web3:'https://paystack.com/buy/opc-premium-store-website-wviynm'};
document.querySelectorAll('.pay').forEach(function(a){var u=LINKS[a.dataset.key];if(u){a.href=u;a.target='_blank';a.rel='noopener';a.textContent=a.dataset.live;}});
function toast(m,t){var d=document.createElement('div');d.className='toast '+(t||'');d.textContent=m;var h=document.getElementById('toasts');if(h){h.appendChild(d);setTimeout(function(){d.remove()},7000);}}
var btns=document.querySelectorAll('.filters button');
btns.forEach(function(b){b.addEventListener('click',function(){btns.forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});document.querySelectorAll('#res-list .res').forEach(function(r){r.hidden=!(b.dataset.f==='all'||r.dataset.cat===b.dataset.f)})})});
var bt=document.getElementById('bank-toggle');
if(bt){var box=document.getElementById('bank-info'),lab=document.getElementById('bank-toggle-label'),line=document.getElementById('bank-line');
var P={name:['OBUGHENI POLYMAN','CONSULTING SERVICES'],ngn:['1031','886124'],usd:['3005','262204'],bank:['U','BA']};
var ngn=function(){return P.ngn.join('')},usd=function(){return P.usd.join('')};
bt.addEventListener('click',function(){var open=box.hidden;line.textContent=open?'Account name: '+P.name.join(' ')+' \u00b7 Bank: '+P.bank.join('')+' \u00b7 Naira account: '+ngn()+' \u00b7 Dollar account: '+usd():'';box.hidden=!open;bt.setAttribute('aria-expanded',String(open));lab.textContent=open?'Hide account details':'Show account details';});
function cp(get,msg){return function(){if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(get()).then(function(){toast(msg,'success')},function(){toast('Could not copy. Select the number and copy it.','error')})}else{toast('Could not copy. Select the number and copy it.','error')}}}
document.getElementById('bank-copy').addEventListener('click',cp(ngn,'Naira account number copied.'));
var u=document.getElementById('bank-copy-usd');if(u)u.addEventListener('click',cp(usd,'Dollar account number copied.'));}
if(location.hash==='#bank-toggle'&&bt){bt.scrollIntoView();}
})();

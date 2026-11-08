(function(){
var LINKS={thesis:'',thesisread:'',toolkit:'https://paystack.shop/pay/iep-toolkit',goals:'https://paystack.shop/pay/iep-goals-ebook',handbook:'https://paystack.shop/pay/5opagi-y6a',faith:'https://selar.com/04967y420v',premium:'',web1:'https://paystack.com/buy/opc-basic-website--1-page-uxkqsq',web2:'https://paystack.com/buy/opc-standard-website--4-pages-puzwfs',web3:'https://paystack.com/buy/opc-premium-store-website-wviynm'};
document.querySelectorAll('.pay').forEach(function(a){var u=LINKS[a.dataset.key];if(u){a.href=u;a.target='_blank';a.rel='noopener';a.textContent=a.dataset.live;}});
function toast(m,t){var d=document.createElement('div');d.className='toast '+(t||'');d.textContent=m;var h=document.getElementById('toasts');if(h){h.appendChild(d);setTimeout(function(){d.remove()},7000);}}
var btns=document.querySelectorAll('.filters button');
btns.forEach(function(b){b.addEventListener('click',function(){btns.forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});document.querySelectorAll('#res-list .res').forEach(function(r){r.hidden=!(b.dataset.f==='all'||r.dataset.cat===b.dataset.f)})})});
var bt=document.getElementById('bank-toggle');
if(bt){var box=document.getElementById('bank-info'),lab=document.getElementById('bank-toggle-label'),line=document.getElementById('bank-line');
var P={name:['Ukwoma Obugheni','Police'],no:['2057','359672'],bank:['U','BA']};var acct=function(){return P.no.join('')};
bt.addEventListener('click',function(){var open=box.hidden;line.textContent=open?'Account name: '+P.name.join(' ')+' \u00b7 Account no: '+acct()+' \u00b7 Bank: '+P.bank.join(''):'';box.hidden=!open;bt.setAttribute('aria-expanded',String(open));lab.textContent=open?'Hide account details':'Show account details';});
document.getElementById('bank-copy').addEventListener('click',function(){if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(acct()).then(function(){toast('Account number copied.','success')},function(){toast('Could not copy. Select the number and copy it.','error')})}else{toast('Could not copy. Select the number and copy it.','error')}});}
if(location.hash==='#bank-toggle'&&bt){bt.scrollIntoView();}
})();

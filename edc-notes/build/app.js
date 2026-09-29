(function(){
  var root=document.documentElement;
  function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
  var t=store('edc-theme'); if(t) root.setAttribute('data-theme',t);
  document.getElementById('theme').onclick=function(){
    var cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
    var nx=cur==='dark'?'light':'dark'; root.setAttribute('data-theme',nx); store('edc-theme',nx)};
  var side=document.getElementById('side');
  document.getElementById('menu').onclick=function(){side.classList.toggle('open')};
  side.addEventListener('click',function(e){if(e.target.tagName==='A'&&innerWidth<=980)side.classList.remove('open')});
  // reveal all answers
  var open=false,btn=document.getElementById('ans');
  btn.onclick=function(){open=!open;document.querySelectorAll('details').forEach(function(d){d.open=open});btn.textContent='Answers: '+(open?'shown':'hidden')};
  // filter chapters
  document.getElementById('q').addEventListener('input',function(e){
    var q=e.target.value.toLowerCase().trim();
    document.querySelectorAll('#side li').forEach(function(li){li.classList.toggle('hide',q&&li.textContent.toLowerCase().indexOf(q)<0)})});
  // progress checkboxes
  var boxes=[].slice.call(document.querySelectorAll('input[data-ch]'));
  function upd(){var n=boxes.filter(function(b){return b.checked}).length;
    document.getElementById('bar').style.width=(boxes.length?100*n/boxes.length:0)+'%';
    document.getElementById('progtxt').textContent=n+' of '+boxes.length+' chapters marked as studied'}
  boxes.forEach(function(b){b.checked=store('edc-done-'+b.dataset.ch)==='1';b.onchange=function(){store('edc-done-'+b.dataset.ch,b.checked?'1':'0');upd()}});
  upd();
  // scroll spy
  var links={};document.querySelectorAll('#side a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
  var heads=[].slice.call(document.querySelectorAll('main h1[id],main h2[id]'));
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
      document.querySelectorAll('#side a.on').forEach(function(a){a.classList.remove('on')});
      var a=links[e.target.id];if(a){a.classList.add('on');var r=a.getBoundingClientRect(),sr=side.getBoundingClientRect();if(r.top<sr.top+40||r.bottom>sr.bottom-40)a.scrollIntoView({block:'center'})}}})},{rootMargin:'-60px 0px -75% 0px'});
    heads.forEach(function(h){io.observe(h)});
  }
  // tap/hover definitions
  var tip=document.createElement('div');tip.id='tip';document.body.appendChild(tip);
  function showTip(el){tip.textContent=el.getAttribute('title')||el.dataset.t;var r=el.getBoundingClientRect();tip.style.display='block';
    tip.style.left=Math.max(8,Math.min(innerWidth-310,r.left))+'px';tip.style.top=(r.bottom+6+tip.offsetHeight>innerHeight?r.top-tip.offsetHeight-6:r.bottom+6)+'px'}
  document.querySelectorAll('abbr[title]').forEach(function(a){a.dataset.t=a.title;a.removeAttribute('title');
    a.addEventListener('mouseenter',function(){showTip(a)});a.addEventListener('mouseleave',function(){tip.style.display='none'});
    a.addEventListener('click',function(e){e.stopPropagation();showTip(a)})});
  document.addEventListener('click',function(){tip.style.display='none'});
})();

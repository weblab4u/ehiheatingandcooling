(function(){
  var t=document.querySelector('.nav-toggle'),m=document.getElementById('mobile-nav');
  function setNav(o){document.body.classList.toggle('nav-open',o);t.setAttribute('aria-expanded',o);t.setAttribute('aria-label',o?'Close menu':'Open menu');m.hidden=!o;}
  if(t&&m){t.addEventListener('click',function(){setNav(m.hidden)});var c=m.querySelector('.m-close');c&&c.addEventListener('click',function(){setNav(false)});}
  // keyboard support for mega menus
  document.querySelectorAll('.has-mega>a').forEach(function(a){a.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){e.preventDefault();var l=a.parentNode.querySelector('.mega a');l&&l.focus();}});});
  // quote forms: light validation + success state (wire action to your form handler / CRM)
  document.querySelectorAll('[data-quote-form]').forEach(function(f){
    f.addEventListener('submit',function(e){
      var ok=true;f.querySelectorAll('[required]').forEach(function(i){if(!i.value.trim()){i.classList.add('error');ok=false;}else i.classList.remove('error');});
      if(f.querySelector('.hp').value){e.preventDefault();return;}
      if(!ok){e.preventDefault();return;}
      if(!f.dataset.live){e.preventDefault();f.querySelector('.form-ok').hidden=false;f.querySelector('button[type=submit]').disabled=true;}
    });
  });
  // sticky CTA hides when a form is on screen
  var s=document.querySelector('.sticky-cta'),forms=document.querySelectorAll('.quote-form');
  if(s&&forms.length&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){var v=es.some(function(x){return x.isIntersecting});s.style.display=v?'none':'';var sn=document.querySelector('.scroll-nav');if(sn&&window.innerWidth<1024)sn.style.display=v?'none':'';});forms.forEach(function(f){io.observe(f)});}

  // scroll reveal with stagger
  var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if('IntersectionObserver' in window&&!rm){
    var els=document.querySelectorAll('.card,.prob,.steps li,.money-grid li,.why-grid li,.review,.area-col,.brand-grid li,.faq,.stats li,.fill-cta,.checklist li,.promo-card');
    var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(el,i){el.classList.add('reveal');el.style.setProperty('--d',(i%6)*0.06+'s');ro.observe(el);});
    // animated counters
    var co=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;co.unobserve(e.target);var el=e.target,m=el.textContent.match(/^([^0-9]*)([0-9][0-9,]*)(.*)$/);if(!m)return;var end=parseInt(m[2].replace(/,/g,''),10),t0=null;
      function step(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1100),v=Math.round(end*(1-Math.pow(1-p,3)));el.textContent=m[1]+v.toLocaleString('en-CA')+m[3];if(p<1)requestAnimationFrame(step);}
      requestAnimationFrame(step);});});
    document.querySelectorAll('.stats strong').forEach(function(el){co.observe(el)});
  }
  // scroll up / down buttons, bottom-left
  var nav=document.createElement('div');nav.className='scroll-nav';
  nav.innerHTML='<button class="sn-up" type="button" aria-label="Scroll to top"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button><button class="sn-down" type="button" aria-label="Scroll to bottom"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12l7 7 7-7"/></svg></button>';
  document.body.appendChild(nav);
  var up=nav.querySelector('.sn-up'),down=nav.querySelector('.sn-down'),beh=rm?'auto':'smooth';
  up.addEventListener('click',function(){window.scrollTo({top:0,behavior:beh})});
  down.addEventListener('click',function(){window.scrollTo({top:document.documentElement.scrollHeight,behavior:beh})});
  function upd(){var y=window.scrollY,max=document.documentElement.scrollHeight-window.innerHeight;up.classList.toggle('show',y>300);down.classList.toggle('show',max-y>300);}
  window.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);upd();

  // review carousel
  document.querySelectorAll('[data-carousel]').forEach(function(c){
    var t=c.querySelector('.rv-track');
    function step(){var card=t.querySelector('.rv-slide');return card?card.getBoundingClientRect().width+16:300}
    c.querySelector('.prev').addEventListener('click',function(){t.scrollBy({left:-step(),behavior:'smooth'})});
    c.querySelector('.next').addEventListener('click',function(){t.scrollBy({left:step(),behavior:'smooth'})});
    t.querySelectorAll('.rv-slide').forEach(function(s){s.addEventListener('click',function(){s.classList.toggle('open')})});
  });
})();

(function(){
  var t=document.querySelector('.nav-toggle'),m=document.getElementById('mobile-nav');
  function setNav(o){document.body.classList.toggle('nav-open',o);t.setAttribute('aria-expanded',o);t.setAttribute('aria-label',o?'Close menu':'Open menu');m.hidden=!o;}
  if(t&&m){t.addEventListener('click',function(){setNav(m.hidden)});var c=m.querySelector('.m-close');c&&c.addEventListener('click',function(){setNav(false)});}
  // keyboard support for mega menus
  document.querySelectorAll('.has-mega>a').forEach(function(a){a.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){e.preventDefault();var l=a.parentNode.querySelector('.mega a');l&&l.focus();}});});
  // quote forms: validate, then send to /api/quote.php (falls back to a normal post without JS)
  document.querySelectorAll('[data-quote-form]').forEach(function(f){
    var pg=f.querySelector('[name=page]');if(pg)pg.value=location.pathname;
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var ok=true,first=null;f.querySelectorAll('[required]').forEach(function(i){if(!i.value.trim()){i.classList.add('error');ok=false;first=first||i;}else i.classList.remove('error');});
      var em=f.querySelector('[name=email]');if(em&&em.value.trim()&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value.trim())){em.classList.add('error');ok=false;first=first||em;}else if(em)em.classList.remove('error');
      var err=f.querySelector('.form-err'),okMsg=f.querySelector('.form-ok'),btn=f.querySelector('button[type=submit]');
      function fail(msg){err.innerHTML=msg+' Or call <a href="tel:+16476945845">1-647-694-5845</a>.';err.hidden=false;btn.disabled=false;btn.classList.remove('sending');}
      if(!ok){first&&first.focus();fail('Please fill in your name, phone and city.');return;}
      if(f.querySelector('.hp').value)return;
      err.hidden=true;btn.disabled=true;btn.classList.add('sending');
      fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}})
        .then(function(r){return r.json().catch(function(){return {ok:false};}).then(function(j){j.status=r.status;return j;});})
        .then(function(j){
          if(j.ok){f.querySelectorAll('input:not([type=hidden]),select,textarea,button').forEach(function(x){x.disabled=true;});okMsg.hidden=false;btn.classList.remove('sending');
            window.dataLayer&&window.dataLayer.push({event:'quote_submitted',form_page:location.pathname});return;}
          if(j.errors){Object.keys(j.errors).forEach(function(k){var i=f.querySelector('[name='+k+']');i&&i.classList.add('error');});fail(j.errors[Object.keys(j.errors)[0]]);return;}
          fail(j.error||'Sorry, that didn\'t go through.');
        })
        .catch(function(){fail('Sorry, that didn\'t go through. Check your connection and try again.');});
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

  // gallery lightbox
  // gallery row arrows
  document.querySelectorAll('.gallery-strip').forEach(function(sec){
    var t=sec.querySelector('.sg-track'),p=sec.querySelector('.sg-prev'),n=sec.querySelector('.sg-next');
    if(!t||!p||!n)return;
    function step(){var c=t.querySelector('.sg-card');return c?(c.getBoundingClientRect().width+18)*2:400}
    function upd(){p.disabled=t.scrollLeft<4;n.disabled=t.scrollLeft+t.clientWidth>=t.scrollWidth-4}
    p.addEventListener('click',function(){t.scrollBy({left:-step(),behavior:'smooth'})});
    n.addEventListener('click',function(){t.scrollBy({left:step(),behavior:'smooth'})});
    t.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);upd();
  });
  var opens=[].slice.call(document.querySelectorAll('.sg-open'));
  if(opens.length){
    var arr='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
    var lb=document.createElement('div');lb.className='lb';lb.hidden=true;lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Photo viewer');
    lb.innerHTML='<img alt=""><p class="lb-cap"></p><button class="lb-close" type="button" aria-label="Close">&#10005;</button><button class="lb-prev" type="button" aria-label="Previous photo">'+arr+'</button><button class="lb-next" type="button" aria-label="Next photo">'+arr+'</button>';
    document.body.appendChild(lb);
    var im=lb.querySelector('img'),cap=lb.querySelector('.lb-cap'),cur=0,last=null;
    function show(i){cur=(i+opens.length)%opens.length;var b=opens[cur];im.src=b.dataset.full;im.alt=b.dataset.alt;cap.textContent=b.dataset.alt+'  ('+(cur+1)+' / '+opens.length+')';}
    function open(i){last=document.activeElement;show(i);lb.hidden=false;document.body.classList.add('lb-open');lb.querySelector('.lb-close').focus();}
    function close(){lb.hidden=true;document.body.classList.remove('lb-open');if(last)last.focus();}
    opens.forEach(function(b,i){b.addEventListener('click',function(){open(i)})});
    lb.querySelector('.lb-close').addEventListener('click',close);
    lb.querySelector('.lb-prev').addEventListener('click',function(e){e.stopPropagation();show(cur-1)});
    lb.querySelector('.lb-next').addEventListener('click',function(e){e.stopPropagation();show(cur+1)});
    lb.addEventListener('click',function(e){if(e.target===lb)close()});
    document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});
    var sx=null;lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
    lb.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)show(cur+(dx<0?1:-1));sx=null});
  }
})();

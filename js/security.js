window.VA={
redact(t){let c=0;[[/[\w.+-]+@[\w-]+\.[\w.]+/g,'[EMAIL]'],[/\b(?:\d[ -]?){13,16}\b/g,'[CARD]'],[/\b\d{3}-\d{2}-\d{4}\b/g,'[SSN]'],[/\b\d{1,3}(?:\.\d{1,3}){3}\b/g,'[IP]'],[/(?:\+?91[ -]?)?[6-9]\d{9}\b/g,'[PHONE]']].forEach(([r,s])=>{t=t.replace(r,()=>{c++;return s})});return{text:t,count:c}},
inject(t){return /(ignore (all |previous |prior )?(instructions|rules)|system prompt|you are now|jailbreak|<script|union\s+select|drop\s+table|;\s*--)/i.test(t)},
esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))},
_log:[],_prev:'GENESIS',
async audit(a){const d=new TextEncoder().encode(this._prev+'|'+new Date().toISOString()+'|'+a);const h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',d))].map(x=>x.toString(16).padStart(2,'0')).join('');this._log.push(`${h.slice(0,12)}  ${a}`);this._prev=h;const e=document.getElementById('aud');if(e)e.textContent=this._log.slice(-8).join('\n')}
};

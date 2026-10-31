const C='va-v6',F=['./','index.html','css/style.css','js/security.js','js/app.js','js/lab.js','js/ai.js','js/viz.js','js/vault.js','js/engine.js','js/v4.js','js/fx.js','icon.svg'];
self.addEventListener('install',e=>e.waitUntil(caches.open(C).then(c=>c.addAll(F))));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET'||new URL(e.request.url).origin!==location.origin)return;e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)))});

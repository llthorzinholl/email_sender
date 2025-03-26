self.addEventListener('install', function(e) {
    console.log('Service Worker: Instalado');
  });
  
  self.addEventListener('fetch', function(e) {
    // Cache opcional — neste caso só deixamos o SW registrado
  });
  
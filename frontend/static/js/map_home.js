
(function(){
  const markers = window.__MARKERS || [];
  const map = L.map('mapHome');
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap' }).addTo(map);

  const markerGroup = L.featureGroup();
  if (markers.length){
    markers.forEach(function(m) {
      L.marker([m.lat, m.lon])
        .bindPopup('#' + m.id + ' - ' + m.title + '<br><small>' + m.category + ' &bull; ' + m.status + '</small>')
        .addTo(markerGroup);
    });
    markerGroup.addTo(map);
    map.fitBounds(markerGroup.getBounds().pad(0.2));
  } else {
    map.setView([-22.0, -43.0], 6);
  }

  var nearbyLayer = L.layerGroup().addTo(map);
  var userMarker = null;

  var btnNearby = document.getElementById('btnNearby');
  if (btnNearby) {
    btnNearby.addEventListener('click', function() {
      if (!navigator.geolocation) {
        alert('Geolocalização não suportada pelo seu navegador.');
        return;
      }
      btnNearby.disabled = true;
      btnNearby.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Localizando...';

      navigator.geolocation.getCurrentPosition(function(pos) {
        var lat = pos.coords.latitude;
        var lon = pos.coords.longitude;

        if (userMarker) map.removeLayer(userMarker);
        userMarker = L.circleMarker([lat, lon], {radius: 10, color: '#0d6efd', fillOpacity: 0.8})
          .bindPopup('Sua localização')
          .addTo(map);

        fetch('/api/nearby?lat=' + lat + '&lon=' + lon + '&radius=5')
          .then(function(r) { return r.json(); })
          .then(function(data) {
            nearbyLayer.clearLayers();
            data.forEach(function(item) {
              L.marker([item.lat, item.lon])
                .bindPopup(
                  '#' + item.id + ' - ' + item.title +
                  '<br><small>' + item.category + ' &bull; ' + item.status + '</small>' +
                  '<br><small>' + item.distance_km + ' km de distância</small>' +
                  '<br><a href="/denuncias/' + item.id + '">Ver detalhes</a>'
                )
                .addTo(nearbyLayer);
            });

            var resultsDiv = document.getElementById('nearbyResults');
            var countSpan = document.getElementById('nearbyCount');
            if (resultsDiv && countSpan) {
              countSpan.textContent = data.length;
              resultsDiv.classList.remove('d-none');
            }

            if (data.length > 0) {
              var bounds = nearbyLayer.getBounds().extend([lat, lon]);
              map.fitBounds(bounds.pad(0.2));
            } else {
              map.setView([lat, lon], 13);
            }

            btnNearby.disabled = false;
            btnNearby.innerHTML = '<i class="bi bi-geo-alt-fill"></i> Próximas a mim';
          });
      }, function() {
        alert('Não foi possível obter sua localização.');
        btnNearby.disabled = false;
        btnNearby.innerHTML = '<i class="bi bi-geo-alt-fill"></i> Próximas a mim';
      });
    });
  }
})();

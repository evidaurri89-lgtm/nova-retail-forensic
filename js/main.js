document.addEventListener('DOMContentLoaded', () => {

  // 1. SCROLL SUAVE
  const scrollBtn = document.getElementById('btn-scroll-map');
  const mapSection = document.getElementById('map-section');
  if (scrollBtn && mapSection) {
    scrollBtn.addEventListener('click', () => {
      mapSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  // 2. FILTROS
  const filterBtns = document.querySelectorAll('.filter-btn');
  const nodeCards  = document.querySelectorAll('.node-card');
  filterBtns.forEach((btn, index) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      nodeCards.forEach(card => {
        let match = false;
        if (index === 0) match = true;
        if (index === 1 && card.classList.contains('critical')) match = true;
        if (index === 2 && card.classList.contains('warning'))  match = true;
        if (index === 3 && card.classList.contains('stable'))   match = true;
        card.style.opacity   = match ? '1'           : '0.25';
        card.style.transform = match ? 'scale(1)'    : 'scale(0.98)';
        card.style.filter    = match ? 'grayscale(0%)' : 'grayscale(100%)';
      });
    });
  });

  // 3. MAPA LEAFLET
  function initMap() {
    if (typeof L === 'undefined') {
      console.error('❌ Leaflet no está disponible');
      return;
    }
    const mapEl = document.getElementById('risk-map');
    if (!mapEl) {
      console.error('❌ No se encontró #risk-map');
      return;
    }

    const stores = [
      { id:'MX-112', name:'Monterrey Cumbres',  lat:25.7197, lng:-100.3632, disc:'20.5%', hora:'05:00 AM', ghost:'Detectados',  tier:1 },
      { id:'MX-034', name:'Saltillo Norte',      lat:25.4832, lng:-100.9737, disc:'19.2%', hora:'05:00 AM', ghost:'Detectados',  tier:1 },
      { id:'MX-076', name:'Torreón Galerías',    lat:25.5428, lng:-103.4068, disc:'18.5%', hora:'05:00 AM', ghost:'Detectados',  tier:1 },
      { id:'MX-025', name:'Nuevo Laredo Centro', lat:27.4769, lng:-99.5152,  disc:'17.8%', hora:'05:00 AM', ghost:'Detectados',  tier:1 },
      { id:'MX-102', name:'Monterrey Sur',       lat:25.6204, lng:-100.2938, disc:'16.4%', hora:'05:00 AM', ghost:'Detectados',  tier:1 },
      { id:'MX-088', name:'Apodaca Aeropuerto',  lat:25.7868, lng:-100.1875, disc:'15.0%', hora:'05:00 AM', ghost:'Detectados',  tier:1 },
      { id:'MX-055', name:'Reynosa Frontera',    lat:26.0820, lng:-98.2720,  disc:'14.2%', hora:'05:00 AM', ghost:'Detectados',  tier:1 },
      { id:'MX-091', name:'Santa Catarina',      lat:25.6736, lng:-100.4582, disc:'13.5%', hora:'05:00 AM', ghost:'Detectados',  tier:1 },
      { id:'MX-089', name:'San Nicolás Centro',  lat:25.7456, lng:-100.2997, disc:'13.0%', hora:'Irregular',ghost:'Riesgo Alto', tier:2 },
      { id:'MX-044', name:'Saltillo Sur',        lat:25.3910, lng:-100.9300, disc:'10.0%', hora:'Irregular',ghost:'Riesgo',      tier:2 },
      { id:'MX-062', name:'Monclova Industrial', lat:26.9097, lng:-101.4218, disc:'8.5%',  hora:'Irregular',ghost:'Watchlist',   tier:2 },
      { id:'MX-041', name:'Guadalupe Sur',       lat:25.6570, lng:-100.2602, disc:'2.1%',  hora:'12:00 PM', ghost:'Limpios',    tier:3 },
      { id:'MX-105', name:'San Pedro Valle',     lat:25.6545, lng:-100.4000, disc:'1.8%',  hora:'14:30 PM', ghost:'Limpios',    tier:3 },
    ];

    const map = L.map('risk-map', {
      center: [25.9, -100.8],
      zoom: 7,
      zoomControl: true,
      attributionControl: false
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);

    setTimeout(() => map.invalidateSize(), 200);

    const colors    = { 1:'#ff3366', 2:'#ffaa00', 3:'#00d2ff' };
    const colorName = { 1:'red',     2:'amber',   3:'blue'    };
    const tierLabel = {
      1:'TIER 1 — INTERVENCIÓN INMEDIATA',
      2:'TIER 2 — PREVENCIÓN REFORZADA',
      3:'TIER 3 — BASELINE NORMAL'
    };

    stores.filter(s => s.tier === 1 && s.id !== 'MX-112').forEach(s => {
      L.polyline([[25.7197,-100.3632],[s.lat,s.lng]], {
        color:'#ff3366', weight:1.5, opacity:0.5, dashArray:'6 10'
      }).addTo(map);
    });

    stores.forEach(s => {
      const color  = colors[s.tier];
      const cName  = colorName[s.tier];
      const radius = s.tier===1 ? 12 : s.tier===2 ? 8 : 6;

      if (s.tier === 1) {
        L.circleMarker([s.lat,s.lng], {
          radius: radius+10, fillColor:'transparent',
          color: color, weight:1, opacity:0.25, fillOpacity:0
        }).addTo(map);
      }

      L.circleMarker([s.lat,s.lng], {
        radius, fillColor: color,
        color:'#ffffff', weight: s.tier===1 ? 1.5 : 0.5,
        opacity:1, fillOpacity: s.tier===1 ? 0.9 : 0.6
      })
      .bindPopup(`
        <div style="min-width:230px;font-family:'Space Grotesk',sans-serif;">
          <div class="map-popup-title">${s.id} · ${s.name}</div>
          <div class="map-popup-row">
            <span class="map-popup-label">Discrepancia</span>
            <span class="map-popup-val ${cName}">${s.disc}</span>
          </div>
          <div class="map-popup-row">
            <span class="map-popup-label">Hora Recepción</span>
            <span class="map-popup-val ${s.tier===1?'red':''}">${s.hora}</span>
          </div>
          <div class="map-popup-row">
            <span class="map-popup-label">Ghost SKUs</span>
            <span class="map-popup-val ${cName}">${s.ghost}</span>
          </div>
          <span class="map-popup-tier ${cName}">${tierLabel[s.tier]}</span>
        </div>
      `, { maxWidth:300 })
      .addTo(map);
    });

    console.log('✅ Mapa cargado con', stores.length, 'nodos.');
  }

  setTimeout(initMap, 400);

  // 4. CONECTAR DATOS REALES (DATA BINDING)
  fetch('data/kpis.json')
    .then(response => {
      if (!response.ok) throw new Error('No se encontró el archivo JSON');
      return response.json();
    })
    .then(kpis => {
      console.log('🔥 Datos forenses reales cargados:', kpis);
      
      const totalRiskEl = document.getElementById('kpi-total-risk');
      if (totalRiskEl) totalRiskEl.innerText = kpis.total_risk_value;

      const maxDiscEl = document.getElementById('kpi-max-disc');
      if (maxDiscEl) maxDiscEl.innerText = kpis.max_discrepancy;

      const criticalStoresEl = document.getElementById('kpi-critical');
      if (criticalStoresEl) criticalStoresEl.innerText = kpis.critical_stores;
      
      const hourEl = document.getElementById('kpi-hour');
      if (hourEl) hourEl.innerText = kpis.pattern_hour;
    })
    .catch(error => {
      console.error('❌ Error cargando los KPIs reales:', error);
    });

});
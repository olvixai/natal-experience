/* ============================================================
 *  NatalExperience CRM — lógica de la app
 * ========================================================== */
'use strict';

const State = {
  token: localStorage.getItem('crm_token') || '',
  nombre: localStorage.getItem('crm_nombre') || '',
  rol: localStorage.getItem('crm_rol') || '',
  usuario: localStorage.getItem('crm_usuario') || '',
  reservas: []
};

// Calendar state
let calView = 'month';
let calDate = new Date();

/* ---------- Cliente API (POST text/plain → sin preflight CORS) ---------- */
async function api(action, payload = {}) {
  if (!CRM_CONFIG.API_URL || CRM_CONFIG.API_URL.indexOf('PEGA_AQUI') === 0) {
    throw new Error('Falta configurar la URL de la API en crm/js/config.js');
  }
  const body = JSON.stringify(Object.assign({ action, token: State.token }, payload));
  const res = await fetch(CRM_CONFIG.API_URL, { method: 'POST', body });
  const data = await res.json();
  if (data && data.expired) { logout(); throw new Error('Sesión expirada, vuelve a entrar'); }
  return data;
}

/* ---------- Utilidades UI ---------- */
const $ = (s, ctx = document) => ctx.querySelector(s);
const $$ = (s, ctx = document) => Array.from(ctx.querySelectorAll(s));

function toast(msg, type = '') {
  const t = $('#toast');
  t.textContent = msg;
  t.className = 'toast' + (type ? ' toast--' + type : '');
  setTimeout(() => t.classList.add('hidden'), 3200);
}
function esc(s) {
  return (s == null ? '' : String(s)).replace(/[&<>"]/g,
    c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}
function fmtMoney(n) {
  const v = parseFloat(String(n).replace(/[^\d.]/g, '')) || 0;
  return v.toLocaleString('pt-BR', { minimumFractionDigits: 0 });
}
function fmtDate(d) {
  if (!d) return '';
  const s = String(d).slice(0, 10);
  const p = s.split('-');
  return p.length === 3 ? `${p[2]}/${p[1]}/${p[0]}` : s;
}

/* ============================================================
 *  LOGIN
 * ========================================================== */
$('#login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = $('#login-btn'), err = $('#login-error');
  err.textContent = '';
  btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
  try {
    const r = await api('login', {
      usuario: $('#login-user').value.trim(),
      password: $('#login-pass').value
    });
    if (!r.ok) { err.textContent = r.error || 'No se pudo entrar'; return; }
    State.token = r.token; State.nombre = r.nombre; State.rol = r.rol; State.usuario = r.usuario;
    localStorage.setItem('crm_token', r.token);
    localStorage.setItem('crm_nombre', r.nombre);
    localStorage.setItem('crm_rol', r.rol);
    localStorage.setItem('crm_usuario', r.usuario);
    enterApp();
  } catch (ex) {
    err.textContent = ex.message;
  } finally {
    btn.disabled = false; btn.textContent = 'Entrar';
  }
});

function logout() {
  ['token', 'nombre', 'rol', 'usuario'].forEach(k => localStorage.removeItem('crm_' + k));
  State.token = ''; State.rol = '';
  $('#view-app').classList.add('hidden');
  $('#view-login').classList.remove('hidden');
}
$('#logout-btn').addEventListener('click', logout);

/* ============================================================
 *  ARRANQUE DE LA APP
 * ========================================================== */
function enterApp() {
  $('#view-login').classList.add('hidden');
  $('#view-app').classList.remove('hidden');
  $('#user-name').textContent = State.nombre + ' · ' + State.rol;
  document.body.classList.toggle('is-admin', State.rol === 'admin');
  $$('.admin-only').forEach(el => el.style.display = State.rol === 'admin' ? '' : 'none');
  fillSelects();
  loadAll();
}

/* ---------- Navegación entre secciones ---------- */
$('#main-nav').addEventListener('click', (e) => {
  const btn = e.target.closest('.navlink');
  if (!btn) return;
  $$('.navlink').forEach(b => b.classList.remove('is-active'));
  btn.classList.add('is-active');
  const sec = btn.dataset.section;
  $$('.section-view').forEach(s => s.classList.add('hidden'));
  $('#section-' + sec).classList.remove('hidden');
  $('#main-nav').classList.remove('open');
  if (sec === 'historial') loadLog();
});
$('#hamb').addEventListener('click', () => $('#main-nav').classList.toggle('open'));

/* ---------- Cargar datos ---------- */
async function loadAll() {
  await Promise.all([loadReservas(), loadDashboard()]);
}

async function loadReservas() {
  try {
    const r = await api('getReservas');
    if (r.ok) { State.reservas = r.reservas; renderKanban(); renderAgenda(); }
  } catch (ex) { toast(ex.message, 'err'); }
}

async function loadDashboard() {
  try {
    const r = await api('getDashboard');
    if (r.ok) renderDashboard(r);
  } catch (ex) { /* silencioso */ }
}

async function loadLog() {
  const cont = $('#logtable');
  cont.innerHTML = '<div class="empty">Cargando…</div>';
  try {
    const r = await api('getLog');
    if (!r.ok) { cont.innerHTML = `<div class="empty">${esc(r.error)}</div>`; return; }
    let html = '<div class="logrow logrow--head"><div>Fecha</div><div>Usuario</div>' +
      '<div>Acción</div><div>Detalle</div></div>';
    if (!r.log.length) html += '<div class="empty">Sin actividad todavía</div>';
    r.log.forEach(l => {
      html += `<div class="logrow">
        <div class="logrow__time">${esc(fmtDateTime(l.fecha))}</div>
        <div class="logrow__user">${esc(l.usuario)}</div>
        <div class="logrow__action">${esc(l.accion)}</div>
        <div>${esc(l.detalle)}</div></div>`;
    });
    cont.innerHTML = html;
  } catch (ex) { cont.innerHTML = `<div class="empty">${esc(ex.message)}</div>`; }
}
function fmtDateTime(d) {
  if (!d) return '';
  const s = String(d);
  return s.indexOf('T') > -1 ? fmtDate(s) + ' ' + s.slice(11, 16) : s;
}

/* ============================================================
 *  DASHBOARD
 * ========================================================== */
function renderDashboard(r) {
  const s = r.stats;
  const cards = [
    { n: s.leadsMes, l: 'Leads este mes' },
    { n: s.porEstado['Confirmado'] || 0, l: 'Confirmadas' },
    { n: s.realizadasMes, l: 'Realizadas este mes' },
    { n: s.totalReservas, l: 'Reservas totales' },
    { n: 'R$ ' + fmtMoney(s.ingresosConfirmados), l: 'Ingresos declarados', money: true }
  ];
  $('#stats').innerHTML = cards.map(c =>
    `<div class="stat${c.money ? ' stat--money' : ''}">
       <div class="stat__num">${esc(c.n)}</div>
       <div class="stat__label">${esc(c.l)}</div></div>`).join('');

  const prox = r.proximas || [];
  $('#proximas').innerHTML = prox.length ? prox.map(p =>
    `<div class="prox">
       <span class="prox__date">${esc(fmtDate(p.fecha))}</span>
       <span class="prox__exc">${esc(p.excursion || '—')}</span>
       <span class="prox__cli">${esc(p.cliente || '')}</span>
       <span class="badge" style="background:${color(p.estado)}">${esc(p.estado)}</span>
     </div>`).join('') : '<div class="empty">No hay excursiones programadas</div>';
}
function color(estado) { return (CRM_CONFIG.COLORES && CRM_CONFIG.COLORES[estado]) || '#6b7a99'; }

/* ============================================================
 *  KANBAN
 * ========================================================== */
function renderKanban() {
  const cont = $('#kanban');
  cont.innerHTML = CRM_CONFIG.ESTADOS.map(estado => {
    const items = State.reservas.filter(r => r.estado === estado);
    const cards = items.map(cardHTML).join('') ||
      '<div class="empty" style="padding:14px;font-size:.82rem">—</div>';
    return `<div class="kcol">
      <div class="kcol__head" style="background:${color(estado)}">
        <span>${esc(estado)}</span><span class="kcol__count">${items.length}</span></div>
      <div class="kcol__body">${cards}</div></div>`;
  }).join('');

  $$('.kcard', cont).forEach(el =>
    el.addEventListener('click', () => openModal(el.dataset.id)));
}

function cardHTML(r) {
  return `<div class="kcard" data-id="${esc(r.id)}" style="border-left-color:${color(r.estado)}">
    <div class="kcard__name">${esc(r.cliente_nombre || 'Sin nombre')}</div>
    <div class="kcard__exc">${esc(r.excursion || '—')}</div>
    ${r.codigo_reserva ? `<div class="kcard__code">${esc(r.codigo_reserva)}</div>` : ''}
    <div class="kcard__row">
      <span class="kcard__origen">${esc(r.origen || '')}</span>
      ${r.precio ? `<span class="kcard__price">R$ ${esc(fmtMoney(r.precio))}</span>` : '<span></span>'}
    </div>
    ${r.fecha_excursion ? `<div class="kcard__row"><span>📅 ${esc(fmtDate(r.fecha_excursion))}</span>
      <span>${r.num_personas ? '👤 ' + esc(r.num_personas) : ''}</span></div>` : ''}
  </div>`;
}

/* ============================================================
 *  AGENDA / CALENDARIO
 * ========================================================== */
const MONTH_NAMES = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
  'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
const DAY_NAMES = ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'];

function renderAgenda() {
  const cont = $('#agenda');
  const monthLabel = MONTH_NAMES[calDate.getMonth()] + ' ' + calDate.getFullYear();
  const weekStart = getWeekStart(calDate);
  const weekLabel = fmtDate(weekStart.toISOString().slice(0,10)) + ' – ' +
    fmtDate(new Date(weekStart.getTime() + 6*86400000).toISOString().slice(0,10));

  cont.innerHTML = `
    <div class="cal-head">
      <div class="cal-nav">
        <button class="btn btn--ghost btn--sm" id="cal-prev">‹</button>
        <span class="cal-title" id="cal-title">${calView === 'month' ? monthLabel : weekLabel}</span>
        <button class="btn btn--ghost btn--sm" id="cal-next">›</button>
      </div>
      <div class="cal-views">
        <button class="btn btn--sm ${calView==='month'?'btn--gold':'btn--ghost'}" id="cal-month-btn">Mês</button>
        <button class="btn btn--sm ${calView==='week'?'btn--gold':'btn--ghost'}" id="cal-week-btn">Semana</button>
      </div>
    </div>
    <div id="cal-grid"></div>`;

  $('#cal-prev').addEventListener('click', () => { calNavigate(-1); renderAgenda(); });
  $('#cal-next').addEventListener('click', () => { calNavigate(1); renderAgenda(); });
  $('#cal-month-btn').addEventListener('click', () => { calView = 'month'; renderAgenda(); });
  $('#cal-week-btn').addEventListener('click', () => { calView = 'week'; renderAgenda(); });

  calView === 'month' ? renderMonth() : renderWeek();
}

function calNavigate(dir) {
  if (calView === 'month') calDate = new Date(calDate.getFullYear(), calDate.getMonth() + dir, 1);
  else calDate = new Date(calDate.getTime() + dir * 7 * 86400000);
}

function getWeekStart(d) {
  const day = d.getDay();
  const diff = day === 0 ? -6 : 1 - day;
  return new Date(d.getFullYear(), d.getMonth(), d.getDate() + diff);
}

function getEventsForDate(dateStr) {
  return State.reservas.filter(r =>
    r.fecha_excursion && r.estado !== 'Cancelado' &&
    String(r.fecha_excursion).slice(0,10) === dateStr);
}

function renderMonth() {
  const grid = $('#cal-grid');
  const year = calDate.getFullYear(), month = calDate.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay  = new Date(year, month + 1, 0);
  const today    = new Date();

  let startOffset = firstDay.getDay();
  startOffset = startOffset === 0 ? 6 : startOffset - 1;

  let html = '<div class="cal-month"><div class="cal-week-row cal-week-header">';
  DAY_NAMES.forEach(d => html += `<div class="cal-day-head">${d}</div>`);
  html += '</div>';

  let cur = new Date(year, month, 1 - startOffset);
  for (let w = 0; w < 6; w++) {
    html += '<div class="cal-week-row">';
    for (let d = 0; d < 7; d++) {
      const inMonth = cur.getMonth() === month;
      const isToday = cur.toDateString() === today.toDateString();
      const dateStr = cur.toISOString().slice(0,10);
      const events  = getEventsForDate(dateStr);
      html += `<div class="cal-day${!inMonth?' cal-day--other':''}${isToday?' cal-day--today':''}">
        <span class="cal-day-num">${cur.getDate()}</span>
        <div class="cal-events">${events.map(r =>
          `<div class="cal-event" data-id="${esc(r.id)}" style="background:${color(r.estado)}" title="${esc(r.cliente_nombre||'')} · ${esc(r.excursion||'')}">
            ${esc(r.cliente_nombre || r.excursion || '—')}
          </div>`).join('')}</div></div>`;
      cur = new Date(cur.getTime() + 86400000);
    }
    html += '</div>';
    if (cur > lastDay && w >= 4) break;
  }
  html += '</div>';
  grid.innerHTML = html;
  $$('.cal-event', grid).forEach(el =>
    el.addEventListener('click', e => { e.stopPropagation(); openModal(el.dataset.id); }));
}

function renderWeek() {
  const grid = $('#cal-grid');
  const weekStart = getWeekStart(calDate);
  const today = new Date();

  let html = '<div class="cal-week-view"><div class="cal-week-row cal-week-header">';
  for (let i = 0; i < 7; i++) {
    const d = new Date(weekStart.getTime() + i*86400000);
    const isToday = d.toDateString() === today.toDateString();
    html += `<div class="cal-day-head${isToday?' cal-day-head--today':''}">${DAY_NAMES[i]}<br><span>${d.getDate()}/${d.getMonth()+1}</span></div>`;
  }
  html += '</div><div class="cal-week-row cal-week-body">';
  for (let i = 0; i < 7; i++) {
    const d = new Date(weekStart.getTime() + i*86400000);
    const isToday = d.toDateString() === today.toDateString();
    const events = getEventsForDate(d.toISOString().slice(0,10));
    html += `<div class="cal-day cal-day--week${isToday?' cal-day--today':''}">
      ${events.length ? events.map(r =>
        `<div class="cal-event cal-event--week" data-id="${esc(r.id)}" style="background:${color(r.estado)}">
          <strong>${esc(r.cliente_nombre||'—')}</strong>
          <span>${esc(r.excursion||'')}</span>
          ${r.num_personas?`<span>${esc(r.num_personas)} pax</span>`:''}
          ${r.precio?`<span>R$ ${esc(fmtMoney(r.precio))}</span>`:''}
        </div>`).join('') : '<div class="cal-no-event"></div>'}
    </div>`;
  }
  html += '</div></div>';
  grid.innerHTML = html;
  $$('.cal-event', grid).forEach(el =>
    el.addEventListener('click', e => { e.stopPropagation(); openModal(el.dataset.id); }));
}

/* ============================================================
 *  MODAL DE RESERVA
 * ========================================================== */
function fillSelects() {
  $('#r-excursion').innerHTML = '<option value=""></option>' +
    CRM_CONFIG.EXCURSIONES.map(e => `<option>${esc(e)}</option>`).join('');
  $('#r-pago').innerHTML = '<option value=""></option>' +
    CRM_CONFIG.FORMAS_PAGO.map(e => `<option>${esc(e)}</option>`).join('');
  $('#r-estado').innerHTML =
    CRM_CONFIG.ESTADOS.concat(['Cancelado']).map(e => `<option>${esc(e)}</option>`).join('');
}

function openModal(id) {
  const r = id ? State.reservas.find(x => String(x.id) === String(id)) : null;
  $('#modal-title').textContent = r ? 'Editar reserva' : 'Nueva reserva';
  $('#r-id').value = r ? r.id : '';
  $('#r-nombre').value = r ? r.cliente_nombre || '' : '';
  $('#r-telefono').value = r ? r.cliente_telefono || '' : '';
  $('#r-email').value = r ? r.cliente_email || '' : '';
  $('#r-excursion').value = r ? r.excursion || '' : '';
  $('#r-fecha').value = r ? String(r.fecha_excursion || '').slice(0, 10) : '';
  $('#r-personas').value = r ? r.num_personas || '' : '';
  $('#r-precio').value = r ? r.precio || '' : '';
  $('#r-pago').value = r ? r.forma_pago || '' : '';
  $('#r-estado').value = r ? r.estado || 'Lead' : 'Lead';
  $('#r-origen').value = r ? r.origen || 'Manual' : 'Manual';
  $('#r-notas').value = r ? r.notas || '' : '';

  const codBox = $('#codigo-box');
  if (r && r.codigo_reserva) { codBox.classList.remove('hidden'); $('#r-codigo').textContent = r.codigo_reserva; }
  else codBox.classList.add('hidden');

  $('#modal').classList.remove('hidden');
}

function closeModal() { $('#modal').classList.add('hidden'); }
$$('[data-close]').forEach(el => el.addEventListener('click', closeModal));
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
$('#new-reserva-btn').addEventListener('click', () => openModal(null));

$('#reserva-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = $('#save-btn');
  btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
  const reserva = {
    id: $('#r-id').value || '',
    cliente_nombre: $('#r-nombre').value.trim(),
    cliente_telefono: $('#r-telefono').value.trim(),
    cliente_email: $('#r-email').value.trim(),
    excursion: $('#r-excursion').value,
    fecha_excursion: $('#r-fecha').value,
    num_personas: $('#r-personas').value,
    precio: $('#r-precio').value,
    forma_pago: $('#r-pago').value,
    estado: $('#r-estado').value,
    origen: $('#r-origen').value,
    notas: $('#r-notas').value.trim()
  };
  try {
    const r = await api('saveReserva', { reserva });
    if (!r.ok) { toast(r.error || 'Error al guardar', 'err'); return; }
    toast('Reserva guardada', 'ok');
    closeModal();
    await loadAll();
  } catch (ex) {
    toast(ex.message, 'err');
  } finally {
    btn.disabled = false; btn.textContent = 'Guardar';
  }
});

/* ============================================================
 *  INICIO
 * ========================================================== */
if (State.token) enterApp();

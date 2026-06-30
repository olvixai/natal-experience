/**
 * ============================================================
 *  NatalExperience CRM  —  Backend (Google Apps Script)
 * ============================================================
 *  Una sola Web App que hace de API sobre Google Sheets.
 *  Todo el CRM (login, reservas, dashboard) pasa por aquí.
 *
 *  PRIMERA VEZ:
 *   1) Edita USUARIOS_INICIALES (abajo) con las contraseñas que quieras.
 *   2) Menú  Ejecutar ▸ setup   (autoriza permisos).
 *   3) Implementar ▸ Nueva implementación ▸ Aplicación web
 *        - Ejecutar como: Yo
 *        - Quién tiene acceso: Cualquier usuario
 *   4) Copia la URL /exec y pégala en  crm/js/config.js
 * ============================================================
 */

const SHEET_ID     = '1K-sHm6QKT78yoUoH-f40df5lb5FS8jJjyOM-HWdy9Vo';
const NOTIFY_EMAIL  = 'natalexperiencetours@gmail.com';

// Sal para hashear contraseñas. Cámbiala una vez y NO la toques más.
const PASSWORD_SALT = 'NEx-2026-rn-buggy-salt';

// Usuarios que se crean al ejecutar setup().  Cambia las contraseñas.
const USUARIOS_INICIALES = [
  { usuario: 'admin', password: 'CAMBIA_ESTO_1', nombre: 'Administrador', rol: 'admin' },
  { usuario: 'socio', password: 'CAMBIA_ESTO_2', nombre: 'Socio',         rol: 'socio' }
];

// Etapas válidas del pipeline (orden importa).
const ESTADOS = ['Lead', 'Contactado', 'Presupuesto', 'Confirmado', 'Pagado', 'Realizado', 'Cancelado'];

// Cabeceras de cada pestaña.
const COLS_RESERVAS = ['id','fecha_creacion','origen','cliente_nombre','cliente_email',
  'cliente_telefono','excursion','fecha_excursion','num_personas','precio','estado',
  'forma_pago','notas','codigo_reserva','creado_por','fecha_actualizacion'];
const COLS_USUARIOS = ['usuario','password_hash','nombre','rol','token','token_expira'];
const COLS_LOG      = ['fecha','usuario','accion','reserva_id','detalle'];


/* ============================================================
 *  ROUTER
 * ========================================================== */
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    // Sin "action" = formulario de contacto público (compatibilidad).
    if (!data.action) return handleContactForm(data);

    switch (data.action) {
      case 'login':        return json(login(data));
      case 'getReservas':  return json(authed(data, getReservas));
      case 'saveReserva':  return json(authed(data, saveReserva));
      case 'getDashboard': return json(authed(data, getDashboard));
      case 'getLog':       return json(authed(data, getLog));
      case 'ping':         return json({ ok: true, ts: Date.now() });
      default:             return json({ ok: false, error: 'Acción desconocida' });
    }
  } catch (err) {
    return json({ ok: false, error: err.message });
  }
}

function doGet() {
  return json({ ok: true, service: 'NatalExperience CRM API' });
}


/* ============================================================
 *  AUTENTICACIÓN
 * ========================================================== */
function hashPwd(pwd) {
  const raw = Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256, PASSWORD_SALT + pwd, Utilities.Charset.UTF_8);
  return raw.map(b => ('0' + (b & 0xff).toString(16)).slice(-2)).join('');
}

function login(data) {
  const sh = sheet('Usuarios');
  const rows = sh.getDataRange().getValues();
  const u = (data.usuario || '').toString().trim().toLowerCase();
  const h = hashPwd(data.password || '');

  for (let i = 1; i < rows.length; i++) {
    if ((rows[i][0] || '').toString().toLowerCase() === u && rows[i][1] === h) {
      const token = Utilities.getUuid();
      const expira = Date.now() + 12 * 60 * 60 * 1000; // 12 h
      sh.getRange(i + 1, 5).setValue(token);
      sh.getRange(i + 1, 6).setValue(expira);
      logAction(rows[i][0], 'login', '', '');
      return { ok: true, token: token, nombre: rows[i][2], rol: rows[i][3], usuario: rows[i][0] };
    }
  }
  return { ok: false, error: 'Usuario o contraseña incorrectos' };
}

// Valida token y ejecuta fn(data, user). Devuelve error si no autorizado.
function authed(data, fn) {
  const sh = sheet('Usuarios');
  const rows = sh.getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][4] && rows[i][4] === data.token) {
      if (Date.now() > Number(rows[i][5])) return { ok: false, error: 'Sesión expirada', expired: true };
      const user = { usuario: rows[i][0], nombre: rows[i][2], rol: rows[i][3] };
      return fn(data, user);
    }
  }
  return { ok: false, error: 'No autorizado', expired: true };
}


/* ============================================================
 *  RESERVAS
 * ========================================================== */
function getReservas(data, user) {
  const sh = sheet('Reservas');
  const rows = sh.getDataRange().getValues();
  const out = [];
  for (let i = 1; i < rows.length; i++) {
    if (!rows[i][0]) continue;
    out.push(rowToObj(rows[i]));
  }
  return { ok: true, reservas: out };
}

function rowToObj(r) {
  const o = {};
  COLS_RESERVAS.forEach((c, idx) => { o[c] = r[idx] instanceof Date ? formatDate(r[idx]) : r[idx]; });
  return o;
}

function formatDate(d) {
  return Utilities.formatDate(d, 'America/Sao_Paulo', "yyyy-MM-dd'T'HH:mm:ss");
}

function saveReserva(data, user) {
  const r = data.reserva || {};
  const sh = sheet('Reservas');
  const rows = sh.getDataRange().getValues();
  const now = new Date();
  let rowIndex = -1;

  if (r.id) {
    for (let i = 1; i < rows.length; i++) {
      if ((rows[i][0] || '').toString() === r.id.toString()) { rowIndex = i + 1; break; }
    }
  }

  // Estado anterior (para detectar el paso a "Confirmado").
  const estadoAnterior = rowIndex > 0 ? rows[rowIndex - 1][COLS_RESERVAS.indexOf('estado')] : '';
  let codigo = rowIndex > 0 ? rows[rowIndex - 1][COLS_RESERVAS.indexOf('codigo_reserva')] : '';

  // Al confirmar por primera vez: generar código y disparar voucher + aviso.
  const seConfirma = r.estado === 'Confirmado' && estadoAnterior !== 'Confirmado';
  if (seConfirma && !codigo) codigo = generarCodigo();

  const registro = {
    id:               r.id || Utilities.getUuid().slice(0, 8),
    fecha_creacion:   rowIndex > 0 ? rows[rowIndex - 1][1] : now,
    origen:           r.origen || (rowIndex > 0 ? rows[rowIndex - 1][2] : 'Manual'),
    cliente_nombre:   r.cliente_nombre || '',
    cliente_email:    r.cliente_email || '',
    cliente_telefono: r.cliente_telefono || '',
    excursion:        r.excursion || '',
    fecha_excursion:  r.fecha_excursion || '',
    num_personas:     r.num_personas || '',
    precio:           r.precio || '',
    estado:           r.estado || 'Lead',
    forma_pago:       r.forma_pago || '',
    notas:            r.notas || '',
    codigo_reserva:   codigo || '',
    creado_por:       rowIndex > 0 ? rows[rowIndex - 1][COLS_RESERVAS.indexOf('creado_por')] : user.usuario,
    fecha_actualizacion: now
  };

  const values = COLS_RESERVAS.map(c => registro[c]);

  if (rowIndex > 0) {
    sh.getRange(rowIndex, 1, 1, values.length).setValues([values]);
    logAction(user.usuario, 'editar', registro.id,
      estadoAnterior !== registro.estado ? (estadoAnterior + ' → ' + registro.estado) : 'datos');
  } else {
    sh.appendRow(values);
    logAction(user.usuario, 'crear', registro.id, registro.estado);
  }

  if (seConfirma) enviarVoucher(registro, user);

  return { ok: true, reserva: registro };
}

function generarCodigo() {
  const n = Math.floor(1000 + Math.random() * 9000);
  const y = new Date().getFullYear().toString().slice(-2);
  return 'NE-' + y + '-' + n;
}

function enviarVoucher(r, user) {
  // 1) Voucher al cliente (si dejó email).
  if (r.cliente_email && /\S+@\S+\.\S+/.test(r.cliente_email)) {
    const asunto = 'Confirmação de Reserva ' + r.codigo_reserva + ' | NatalExperience Tours';
    const cuerpo =
      'Olá ' + r.cliente_nombre + ',\n\n' +
      'A sua reserva está confirmada! Aqui estão os detalhes:\n\n' +
      'Código de reserva: ' + r.codigo_reserva + '\n' +
      'Experiência: ' + r.excursion + '\n' +
      (r.fecha_excursion ? 'Data: ' + r.fecha_excursion + '\n' : '') +
      (r.num_personas ? 'Pessoas: ' + r.num_personas + '\n' : '') +
      (r.precio ? 'Valor: R$ ' + r.precio + '\n' : '') +
      '\nGuarde este código. Em breve entraremos em contacto com os últimos detalhes.\n\n' +
      'Obrigado por escolher a NatalExperience Tours!\n';
    try {
      GmailApp.sendEmail(r.cliente_email, asunto, cuerpo,
        { name: 'NatalExperience Tours', replyTo: NOTIFY_EMAIL });
    } catch (err) { /* email inválido: no romper el guardado */ }
  }

  // 2) Aviso al administrador (control).
  GmailApp.sendEmail(NOTIFY_EMAIL,
    '[CRM] Reserva CONFIRMADA ' + r.codigo_reserva,
    'Una reserva se ha confirmado en el CRM:\n\n' +
    'Código: ' + r.codigo_reserva + '\n' +
    'Cliente: ' + r.cliente_nombre + ' (' + r.cliente_telefono + ')\n' +
    'Excursión: ' + r.excursion + '\n' +
    'Fecha: ' + r.fecha_excursion + '\n' +
    'Personas: ' + r.num_personas + '\n' +
    'Precio: R$ ' + r.precio + '\n' +
    'Forma de pago: ' + r.forma_pago + '\n' +
    'Confirmada por: ' + user.nombre + ' (' + user.usuario + ')\n');
}


/* ============================================================
 *  DASHBOARD  +  LOG
 * ========================================================== */
function getDashboard(data, user) {
  const sh = sheet('Reservas');
  const rows = sh.getDataRange().getValues();
  const idxEstado = COLS_RESERVAS.indexOf('estado');
  const idxPrecio = COLS_RESERVAS.indexOf('precio');
  const idxFechaEx = COLS_RESERVAS.indexOf('fecha_excursion');
  const idxCreada = COLS_RESERVAS.indexOf('fecha_creacion');

  const porEstado = {};
  ESTADOS.forEach(s => porEstado[s] = 0);
  let ingresosConfirmados = 0, totalReservas = 0;
  let leadsMes = 0, realizadasMes = 0;
  const ahora = new Date();
  const mesActual = ahora.getFullYear() + '-' + (ahora.getMonth() + 1);
  const proximas = [];

  for (let i = 1; i < rows.length; i++) {
    if (!rows[i][0]) continue;
    totalReservas++;
    const estado = rows[i][idxEstado];
    if (porEstado[estado] !== undefined) porEstado[estado]++;

    const precio = parseFloat((rows[i][idxPrecio] || '').toString().replace(/[^\d.]/g, '')) || 0;
    if (estado === 'Confirmado' || estado === 'Pagado' || estado === 'Realizado') ingresosConfirmados += precio;

    const creada = rows[i][idxCreada];
    if (creada instanceof Date && (creada.getFullYear() + '-' + (creada.getMonth() + 1)) === mesActual) {
      leadsMes++;
      if (estado === 'Realizado') realizadasMes++;
    }

    // Próximas excursiones (fecha futura, no cancelada).
    const fx = rows[i][idxFechaEx];
    if (fx && estado !== 'Cancelado' && estado !== 'Realizado') {
      proximas.push({
        codigo: rows[i][COLS_RESERVAS.indexOf('codigo_reserva')],
        cliente: rows[i][COLS_RESERVAS.indexOf('cliente_nombre')],
        excursion: rows[i][COLS_RESERVAS.indexOf('excursion')],
        fecha: (fx instanceof Date) ? formatDate(fx) : fx,
        estado: estado
      });
    }
  }

  proximas.sort((a, b) => (a.fecha > b.fecha ? 1 : -1));

  return {
    ok: true,
    stats: {
      porEstado: porEstado,
      ingresosConfirmados: ingresosConfirmados,
      totalReservas: totalReservas,
      leadsMes: leadsMes,
      realizadasMes: realizadasMes
    },
    proximas: proximas.slice(0, 10)
  };
}

function getLog(data, user) {
  if (user.rol !== 'admin') return { ok: false, error: 'Solo el administrador puede ver el historial' };
  const sh = sheet('Log');
  const rows = sh.getDataRange().getValues();
  const out = [];
  for (let i = Math.max(1, rows.length - 200); i < rows.length; i++) {
    out.push({
      fecha: rows[i][0] instanceof Date ? formatDate(rows[i][0]) : rows[i][0],
      usuario: rows[i][1], accion: rows[i][2], reserva_id: rows[i][3], detalle: rows[i][4]
    });
  }
  return { ok: true, log: out.reverse() };
}

function logAction(usuario, accion, reservaId, detalle) {
  try { sheet('Log').appendRow([new Date(), usuario, accion, reservaId, detalle]); }
  catch (err) { /* nunca bloquear por el log */ }
}


/* ============================================================
 *  FORMULARIO DE CONTACTO (público)  →  entra como Lead
 * ========================================================== */
function handleContactForm(data) {
  const sh = sheet('Reservas');
  const now = new Date();
  const id = Utilities.getUuid().slice(0, 8);
  const registro = {
    id: id, fecha_creacion: now, origen: 'Web',
    cliente_nombre: data.name || '', cliente_email: data.email || '',
    cliente_telefono: data.phone || '', excursion: data.interest || '',
    fecha_excursion: '', num_personas: '', precio: '', estado: 'Lead',
    forma_pago: '', notas: data.message || '', codigo_reserva: '',
    creado_por: 'web', fecha_actualizacion: now
  };
  sh.appendRow(COLS_RESERVAS.map(c => registro[c]));
  logAction('web', 'lead-web', id, data.interest || '');

  GmailApp.sendEmail(NOTIFY_EMAIL, '[NatalExperience] Nuevo lead recibido',
    'Nuevo lead desde la web:\n\n' +
    'Nombre: ' + data.name + '\nEmail: ' + data.email + '\nTeléfono: ' + data.phone +
    '\nInterés: ' + data.interest + '\nMensaje: ' + data.message +
    '\n\nFecha: ' + now.toLocaleString('pt-BR'));

  return json({ success: true });
}


/* ============================================================
 *  UTILIDADES
 * ========================================================== */
function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function sheet(name) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  return sh;
}


/* ============================================================
 *  SETUP  —  ejecutar UNA vez desde el editor
 * ========================================================== */
function setup() {
  const ss = SpreadsheetApp.openById(SHEET_ID);

  // Reservas
  let sh = ss.getSheetByName('Reservas') || ss.insertSheet('Reservas');
  if (sh.getLastRow() === 0) sh.appendRow(COLS_RESERVAS);

  // Usuarios
  sh = ss.getSheetByName('Usuarios') || ss.insertSheet('Usuarios');
  sh.clear();
  sh.appendRow(COLS_USUARIOS);
  USUARIOS_INICIALES.forEach(u => {
    sh.appendRow([u.usuario.toLowerCase(), hashPwd(u.password), u.nombre, u.rol, '', '']);
  });

  // Log
  sh = ss.getSheetByName('Log') || ss.insertSheet('Log');
  if (sh.getLastRow() === 0) sh.appendRow(COLS_LOG);

  Logger.log('Setup completado. Usuarios creados: ' +
    USUARIOS_INICIALES.map(u => u.usuario).join(', '));
}

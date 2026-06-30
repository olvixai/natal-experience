/* ============================================================
 *  CONFIGURACIÓN DEL CRM
 *  Pega aquí la URL /exec de tu Web App de Apps Script.
 * ========================================================== */
const CRM_CONFIG = {
  // Mismo backend que el formulario de contacto (un solo Apps Script para todo).
  API_URL: 'https://script.google.com/macros/s/AKfycbwVj1RiePDs5QZAmSpU4H6kFAZM74EyBinIwKa1pD0YJCnnnU83hQhJTYV9zcjFuT5z/exec',

  // Etapas del pipeline (puedes reordenar o renombrar, pero deben
  // coincidir con las del backend Code.gs → ESTADOS).
  ESTADOS: ['Lead', 'Contactado', 'Presupuesto', 'Confirmado', 'Pagado', 'Realizado'],

  // Lista de excursiones para el desplegable (edítala libremente).
  EXCURSIONES: [
    'Litoral Norte Completo',
    'Litoral Norte Especial',
    'Litoral Norte Alternativo',
    'Passeio para Pipa (Litoral Sul)',
    'Rota Norte + Sobrevoo de Helicóptero',
    'Transfer VIP',
    'Roteiro sob medida',
    'Outro'
  ],

  // Formas de pago.
  FORMAS_PAGO: ['Pix', 'Efectivo', 'Tarjeta', 'Transferencia', 'Otro'],

  // Color por etapa (para las columnas del pipeline).
  COLORES: {
    'Lead':        '#6b7a99',
    'Contactado':  '#4a90d9',
    'Presupuesto': '#c9a84c',
    'Confirmado':  '#2e9e6b',
    'Pagado':      '#1da851',
    'Realizado':   '#7b5cd6',
    'Cancelado':   '#b04a4a'
  }
};

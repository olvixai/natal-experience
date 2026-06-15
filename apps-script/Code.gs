const SHEET_ID = '1K-sHm6QKT78yoUoH-f40df5lb5FS8jJjyOM-HWdy9Vo';
const NOTIFY_EMAIL = 'natalexperiencetours@gmail.com';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    // Save to Sheets
    const sheet = SpreadsheetApp.openById(SHEET_ID).getActiveSheet();
    sheet.appendRow([
      new Date(),
      data.name || '',
      data.email || '',
      data.phone || '',
      data.interest || '',
      data.message || ''
    ]);

    // Add headers if first row is empty
    if (sheet.getLastRow() === 1) {
      sheet.insertRowBefore(1);
      sheet.getRange(1, 1, 1, 6).setValues([['Fecha', 'Nombre', 'Email', 'Teléfono', 'Interés', 'Mensaje']]);
    }

    // Send notification email
    GmailApp.sendEmail(
      NOTIFY_EMAIL,
      '🌟 Nuevo lead - NatalExperience Tours',
      `Nuevo mensaje recibido desde el formulario de contacto:\n\n` +
      `Nombre: ${data.name}\n` +
      `Email: ${data.email}\n` +
      `Teléfono: ${data.phone}\n` +
      `Interés: ${data.interest}\n` +
      `Mensaje: ${data.message}\n\n` +
      `Fecha: ${new Date().toLocaleString('pt-BR')}`
    );

    return ContentService
      .createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

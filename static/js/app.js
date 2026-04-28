/* =====================================================
   Consultorio Ginecológico — JS principal
   ===================================================== */

// Registrar Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/js/sw.js')
      .then(reg => console.log('SW registrado:', reg.scope))
      .catch(err => console.warn('SW error:', err));
  });
}

// Auto-cerrar alertas después de 4 segundos
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert-dismissible.auto-close').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });
});

const filas = document.querySelector('#filas');
const detalle = document.querySelector('#detalle');
const formulario = document.querySelector('#edicion');
const confirmacion = document.querySelector('#confirmar');
let seleccionado;

const numero = valor => new Intl.NumberFormat('es-AR', {maximumFractionDigits: 3}).format(valor);
const fecha = valor => new Intl.DateTimeFormat('es-AR', {dateStyle: 'long', timeStyle: 'short'}).format(new Date(valor));
async function api(url, opciones = {}) {
  const respuesta = await fetch(url, {headers: {'Content-Type': 'application/json'}, ...opciones});
  const datos = await respuesta.json();
  if (!respuesta.ok) throw new Error(datos.error || 'No se pudo completar la operación');
  return datos;
}
function toast(mensaje, tipo = 'ok') {
  const nodo = document.createElement('div'); nodo.className = `toast ${tipo}`; nodo.textContent = mensaje;
  document.querySelector('#alertas').append(nodo); setTimeout(() => nodo.remove(), 6000);
}
async function cargar() {
  const insumos = await api('/api/insumos'); filas.replaceChildren();
  insumos.forEach(insumo => {
    const fila = document.createElement('tr'); fila.tabIndex = 0; fila.className = 'insumo';
    fila.innerHTML = `<td><strong>${insumo.nombre}</strong><small>${insumo.codigo}</small></td><td>${insumo.categoria}</td><td>${insumo.ubicacion}</td><td>${numero(insumo.stock)} ${insumo.unidad}</td><td><span class="estado ${insumo.stock_bajo ? 'bajo' : ''}">${insumo.stock_bajo ? 'Stock bajo' : 'Disponible'}</span></td>`;
    fila.addEventListener('click', () => abrir(insumo.id));
    fila.addEventListener('keydown', evento => { if (evento.key === 'Enter') abrir(insumo.id); }); filas.append(fila);
    if (insumo.stock_bajo) toast(`Stock bajo: ${insumo.nombre} tiene ${numero(insumo.stock)} ${insumo.unidad}; mínimo ${numero(insumo.minimo)}. Se envió una notificación de aviso.`, 'aviso');
  });
}
async function abrir(id) {
  seleccionado = await api(`/api/insumos/${id}`); document.querySelector('#titulo').textContent = seleccionado.nombre;
  document.querySelector('#caracteristicas').innerHTML = `<div><dt>Código</dt><dd>${seleccionado.codigo}</dd></div><div><dt>Unidad</dt><dd>${seleccionado.unidad}</dd></div><div><dt>Stock actual</dt><dd>${numero(seleccionado.stock)}</dd></div><div><dt>Rango</dt><dd>${numero(seleccionado.minimo)} – ${numero(seleccionado.maximo)}</dd></div>`;
  document.querySelector('#fecha').textContent = `Última modificación: ${fecha(seleccionado.actualizado_en)}`;
  ['categoria','ubicacion','minimo','maximo'].forEach(campo => formulario.elements[campo].value = seleccionado[campo]); detalle.showModal();
}
formulario.addEventListener('submit', async evento => { evento.preventDefault();
  const datos = Object.fromEntries(new FormData(formulario)); datos.minimo = Number(datos.minimo); datos.maximo = Number(datos.maximo);
  try { seleccionado = await api(`/api/insumos/${seleccionado.id}`, {method:'PATCH', body:JSON.stringify(datos)}); detalle.close(); toast('Producto actualizado correctamente.'); await cargar(); } catch (error) { toast(error.message, 'error'); }
});
document.querySelector('.cerrar').onclick = () => detalle.close();
document.querySelector('#borrar').onclick = () => confirmacion.showModal();
document.querySelector('#cancelar').onclick = () => confirmacion.close();
document.querySelector('#confirmar-borrado').onclick = async () => { try { await api(`/api/insumos/${seleccionado.id}`, {method:'DELETE'}); confirmacion.close(); detalle.close(); toast('Producto eliminado por completo.'); await cargar(); } catch(error) { toast(error.message, 'error'); } };
document.querySelector('#actualizar').onclick = cargar;
cargar().catch(error => toast(error.message, 'error'));

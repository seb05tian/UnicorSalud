function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  const csrftoken = getCookie('csrftoken');
  const API_URL = '/api/asignaturas/';
  const form = document.getElementById('form-asignatura');
  const lista = document.getElementById('lista-asignaturas');
  
  const cargarAsignaturas = () => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        lista.innerHTML = '';
        data.forEach(asig => {
          lista.innerHTML += `
            <li>
              ${asig.codigo} - ${asig.nombre} - Nivel: ${asig.nivel}
              <span>
                <button onclick="editarAsignatura(${asig.id})">Editar</button>
                <button onclick="eliminarAsignatura(${asig.id})">Eliminar</button>
              </span>
            </li>
          `;
        });
      })
      .catch(error => alert("Error cargando asignaturas: " + error));
  };
  
  form.onsubmit = e => {
    e.preventDefault();
    const id = document.getElementById('id').value;
    const metodo = id ? 'PUT' : 'POST';
    const url = id ? `${API_URL}${id}/` : API_URL;
  
    fetch(url, {
      method: metodo,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        codigo: document.getElementById('codigo').value,
        nombre: document.getElementById('nombre').value,
        nivel: document.getElementById('nivel').value,
        descripcion: document.getElementById('descripcion').value,
        programa: document.getElementById('programa').value
      })
    })
    .then(() => {
      form.reset();
      cargarAsignaturas();
    })
    .catch(error => alert("Error guardando asignatura: " + error));
  };
  
  const editarAsignatura = id => {
    fetch(`${API_URL}${id}/`)
      .then(res => res.json())
      .then(asig => {
        document.getElementById('id').value = asig.id;
        document.getElementById('codigo').value = asig.codigo;
        document.getElementById('nombre').value = asig.nombre;
        document.getElementById('nivel').value = asig.nivel;
        document.getElementById('descripcion').value = asig.descripcion || '';
        document.getElementById('programa').value = asig.programa;
      })
      .catch(error => alert("Error cargando asignatura: " + error));
  };
  
  const eliminarAsignatura = id => {
    if (confirm("¿Está seguro de eliminar esta asignatura?")) {
      fetch(`${API_URL}${id}/`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
      .then(() => cargarAsignaturas())
      .catch(error => alert("Error eliminando asignatura: " + error));
    }
  };
  
  cargarAsignaturas();
  
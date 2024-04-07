let productos = [];
let categorias = [];
let mensajesValidarDatos = null;
let base64URL = null;

function login() {
  const usuario = document.getElementById("correo");
  const password = document.getElementById("contraseña");
  if (!usuario.value || !password.value) {
    swal.fire(
      "Iniciar sesión",
      "Por favor, complete todos los campos",
      "warning"
    );
    return;
  }
  const user = {
    usuario: correo.value,
    password: contraseña.value,
  };
  const url = "/";
  fetch(url, {
    method: "POST",
    body: JSON.stringify(user),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((respuesta) => {
      if (!respuesta.ok) {
        throw new Error("Error en la solicitud");
      }
      return respuesta.json();
    })
    .then((result) => {
      console.log(result);
      if (result.estado) {
        location.href = "/listaProductos";
      } else {
        swal.fire("Iniciar sesión", result.mensaje, "warning");
      }
    })
    .catch((error) => {
      console.error("Error:", error.message);
      swal.fire(
        "Iniciar sesión",
        "Se produjo un error al intentar iniciar sesión",
        "error"
      );
    });
}

function visualizarFoto(event) {
  var imagen = document.getElementById("imagenPreview");
  imagen.src = URL.createObjectURL(event.target.files[0]);
}

// Petición al servidor para editar un producto de acuerdo a su id

function editarProducto() {
  const producto = {
    id: idProducto.value,
    codigo: txtCodigo.value,
    nombre: txtNombre.value,
    precio: txtPrecio.value,
    categoria: cbCategoria.value,
  };
  const foto = {
    foto: base64URL,
  };
  const datos = {
    producto: producto,
    foto: foto,
  };
  const url = "/editarProducto";
  fetch(url, {
    method: "PUT",
    body: JSON.stringify(datos),
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then(respuesta => respuesta.json())
  .then(resultado => {
    console.log(resultado);
    if (resultado.estado) {
      swal.fire({
        title: resultado.mensaje,
        confirmButtonText: 'Continuar',
        icon: 'succes',
      }).then((result) => {
        if (result.isConfirmed) {
          location.href = '/listarProductos'
        }
      })
    } else {
      swal.fire('Editar producto', resultado.mensaje, 'warning')
    }
  })
}


/**
 * Función que realiza una petición al servidor para eliminar un productode acuerdo a su id
 * @param {*} id
 */

function eliminarJson(id) {
  Swal.fire({
    title: '¿Está seguro de eliminar el producto?',
    showDenyButton: true,
    confirmButtonText: 'SI',
    denyButtonText: 'NO'    
  }).then((result) => {
    if (result.isConfirmed) {
      url = '/eliminarJson/' + id
      fetch(url, {
        method: DELETE,        
        headers: {
          'Content-Type': 'application/json',
        }
      })
      .then(respuesta => respuesta.json())
      .then(resultado => {
        if (resultado.estado) {
          Swal.fire({
            title: resultado.mensaje,
            confirmButtonText: 'Continuar',
            icon: 'success'
          }).then((result) => {
            if (result.isConfirmed) {
              location.href = '/listaProductos'
            }
          })
        } else {
          swal.fire('Eliminar producto', resultado.mensaje, 'info')
        }
      })
      .catch(error => {
        console.error(error);
      })
    }
  })
}
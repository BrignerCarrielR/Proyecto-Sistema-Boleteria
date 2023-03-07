class Venta {
    constructor(save) {
        this.save = save
        this.ban = false; // Bandera para que al guardar, pueda estar en true y evitar el preventDefault

        this.datos = {
            chofer: '',
            copiloto: '',
            oficinista: '',
            bus: '',
            ruta: '',
            fecha_hora: '',
            total: 0,
            boleto: [],
        };
        this.capacidad = 0;
    };

    agreBus(bus) { // Se agrega el ID del bus junto a su capacidad.
        this.datos.bus = bus.id;
        this.capacidad = bus.capacidad;
    };

    presentarOptionsDestino(dato) { // Presenta las opciones para el select de Destinos.
        let destin = document.getElementById('idDestino'); // Se toma el select.
        destin.innerHTML = ''; // Se lo vacía
        destin.innerHTML = '<option value="">----</option>';
        dato.forEach((valor) => { // Se itera los destinos y se va agregando un option por cada destino.
            destin.innerHTML += `
                <option>${valor.name}</option>`
        });
    };

    SeparadorDestinosCostos(origen, destinos) { // Separa los destinos y costos en un diccionario por nombre y costo.
        let data = []; //Aquí se guardarán los destinos.
        for (let valor of destinos) { // Se itera la lista donde cada valor tendrá el destino y costo separado por una coma.
            let dato = {}; //Aquí se guardará el destino de la iteración.
            let a = valor.split(","); // Se separa en un arreglo el valor de la iteración
            dato.name = (origen + " - " + a[0]); // Aquí concatenamos el origen para que quede como: origen - destino.
            dato.costo = parseFloat(a[1]);
            data = [...data, dato]; // Acumulamos el destino.
        }
        return data;
    };

    aggDetalleVenta(dato) { // Se hace registro de cada boleto añadido.
        this.datos.boleto = [
            ...this.datos.boleto,
            dato
        ];
        this.Calculartotal();
        this.presentarTablaBoleto();
    };


    Calculartotal() { // Calcula el total.
        this.datos.total = 0;
        this.datos.boleto.forEach((item) => { // Se itera y se va acumulando el total de los boletos.
            this.datos.total += item.costo;
        });
        this.datos.total = this.datos.total.toFixed(2); // toFixed permite tomar solo dos dígitos como decimal.
    }

    presentarTablaBoleto() { // Permite la presentación de los boletos en la tabla del html.
        let boleto = document.getElementById('idTablaBoletos'); // Tomamos el body de la tabla boletos.
        boleto.innerHTML = ''; // Vacía el contenido de la tabla.
        this.datos.boleto.forEach((item) => { // Itera el contenido de los boletos y los va acumulando dentro de la tabla .
            boleto.innerHTML += `
                <tr>
                    <th class="text-center" scope="row">${item.asiento}</th>
                    <td>${item.pasajero}</td>
                    <td>${item.destino}</td>
                    <td>$ ${item.costo}</td>
                    <td>${item.hora.split(" ")[1]}</td>
                </tr>`
        }); // En item.hora.split dividimos la fecha en un arreglo,
        // en la primera posición la fecha y en la segunda la hora,
        // por eso tomamos la posición 1, ya que es de la hora.

        // Presentamos el total en el html
        document.getElementById('textTotal').value = "$ " + this.datos.total + " ctvs";
        // Se suma +1 a la cantidad de boletos que haya
        // para presentarlo en el html como el siguiente asiento a vender.
        document.getElementById('idAsiento').value = this.datos.boleto.length + 1;
    }

    registroVenta() { // Se hace el registro con un fetch async await.
        // Se toman los select de ruta, chofer y copiloto.
        const $cboRuta = document.getElementById('cboRuta');
        const $cboChofer = document.getElementById('cboChofer');
        const $cboCopi = document.getElementById('cboCopiloto');


        // Aquí guardamos en la variable de clase datos los valores faltantes.
        this.datos.ruta = $cboRuta.options[$cboRuta.selectedIndex].value;
        this.datos.chofer = $cboChofer.options[$cboChofer.selectedIndex].value;
        this.datos.copiloto = $cboCopi.options[$cboCopi.selectedIndex].value;
        // Tomamos la fecha y le quitamos la coma eje: '2/3/2023, 21:13:05' ==> '2/3/2023 21:13:05'.
        this.datos.fecha_hora = document.getElementById('fecha_hora').value.replaceAll(',', '');
        // Tomamos el ID de oficinista y le separamos con split para tomar su primer valor que es la ID.
        this.datos.oficinista = idOfi.id.split(",")[0];
        this.datos.action = document.querySelector('[name=action]').value;
        let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const grabarVenta = async (url) => { // Función del async.
            try {
                const res = await fetch(url, // Función del fetch.
                    {
                        method: 'POST',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrf,
                        },
                        body: JSON.stringify(this.datos) // Creo aquí convierte tus datos a un archivo JSON.
                    });
                const post = await res.json(); // Espera la respuesta del fetch, para enviarla.

            } catch (error) {
                console.log("error=>", error);
                alert(error)
            }
        };
        // Siempre que la venta esté completa con todos sus datos, se cumplirá y grabará.
        if (this.datos.ruta && this.datos.chofer && this.datos.copiloto && this.datos.bus) {
            grabarVenta(this.save) // Llama a la función de arriba para grabar.
                .then(() => { // Con esto devolvemos el enlace para redireccionar cuando termine la grabación.
                        location.href = "/list_Venta_user" // Enlace de redireccionamiento.
                        return false
                    }
                )
        } else {
            this.ban = false
            alert('Rellene toda la venta por favor!')
        }
    }

    DeshabilitarPasaje(lista, destino) { // Deshabilita el pasaje cuando no está seleccionado la ruta o el bus.
        destino.setAttribute("disabled", "true"); // Inhabilita el select de destino.
        destino.value = "" //Limpia la opción de destino.
        document.querySelector(lista[0]).value = "" // Limpia el select.
        document.querySelector(lista[0]).removeAttribute("disabled"); //Habilita los select de bus y ruta.
        document.querySelector(lista[1]).setAttribute("class", '');// Agranda la columna horizontalmente de los seletc.
        document.querySelector(lista[2]).setAttribute("class", '');// Oculta el div del btn de X.
        document.querySelector(lista[3]).setAttribute("style", 'display: none');  // Oculta el btn de X.
        document.querySelector('#inputPasajero').setAttribute("disabled", "true"); // Inhabilita el input de pasajero.
        document.querySelector('#idModoPago').setAttribute("disabled", "true"); // Inhabilita el select modo de pago.
        document.querySelector('#inputPasajero').value = ""; // Limpia el input de pasajero.
        document.querySelector('#idCosto').value = "$ 0.00"; // Limpia el input de costo.
    }

    creacionBotonDelete(lista, selectAgarrado) {
        selectAgarrado.setAttribute("disabled", true);
        document.querySelector(lista[0]).setAttribute("class", 'col-10 text-center');
        document.querySelector(lista[1]).setAttribute("class", 'col-2');
        document.querySelector(lista[2]).setAttribute("style", '');
    }

}

//_________________________________________DOM________________________________________________

document.addEventListener("DOMContentLoaded", e => {
        let venta = new Venta(save);

        let fecha = new Date;
        let $fecha_hora = document.getElementById('fecha_hora'); // Toma la etiqueta de fecha_hora.
        $fecha_hora.value = fecha.toLocaleString(); // Genera una fecha del momento actual y la presenta a esa etiqueta.

        //Con esta función onbeforeunload le indicamos que no pueda recargar la página siempre y cuando no haya boletos vendidos
        window.onbeforeunload = function (e) {
            if (venta.ban == false && venta.datos.boleto.length>0) {
                e.preventDefault();
                console.log(e);
                return "Tienes cambios sin guardar";
            }
        };

        document.getElementById('idOficinista').value = idOfi.id.split(",")[1]; //Asigno el nombre del oficinista.
        let $rutas = document.getElementById('cboRuta'); // Tomamos el select de ruta.
        let $destin = document.querySelector("#idDestino"); // Tomamos el select de destino.
        let dataDestino = []; // Los destinos a guardar para posteriormente presentar dependiendo de su ruta.

        document.addEventListener('change', (evt) => { // Cuando haya un cambio (change),
            // dependiendo de la etiqueta se hará algo.
            let $cboAgarrado = evt.target; // Se crea una variable que tomará el valor de un select, puede ser bus o ruta.
            if (evt.target.matches("#cboBus")) { //  Aquí es para el select de bus.
                //Toma la data-ajson de la option seleccionada.
                let buses = $cboAgarrado.options[$cboAgarrado.selectedIndex].getAttribute('data-ajson');

                if ($cboAgarrado.options[$cboAgarrado.selectedIndex].value != "") {
                    let bus = JSON.parse(buses); //Convierte a un JSON
                    bus.id = parseInt(bus.id); //Convierte a un int el id
                    bus.capacidad = parseInt(bus.capacidad); //Convierte a un int la capacidad
                    venta.agreBus(bus); //Agrega el bus seleccionado
                    let variables = ['#colBus', '#colBtnBus', '#btnDeleteBus'];
                    venta.creacionBotonDelete(variables, $cboAgarrado);

                    if ($rutas.options[$rutas.selectedIndex].value != "") {
                        $destin.removeAttribute("disabled");
                        document.querySelector('#inputPasajero').removeAttribute("disabled");
                        document.querySelector('#idModoPago').removeAttribute("disabled");
                    }

                }


            } else if (evt.target.matches("#cboRuta")) {
                document.getElementById('idCosto').value = "$" + " 0.00"; // Limpiamos el valor de Costo

                if ($cboAgarrado.options[$cboAgarrado.selectedIndex].value !== "") {
                    $destin.innerHTML = ``; // Limpiamos las opciones de destino
                    let variables = ['#colRuta', '#colBtnRuta', '#btnDeleteRuta'];
                    venta.creacionBotonDelete(variables, $cboAgarrado);

                    //Aquí crea los valores de las opciones de destino
                    if ($cboAgarrado.options[$cboAgarrado.selectedIndex].value == 1) { // Si el select es igual a 1...
                        let destinos = ["Posa Seca,0.60", "Eden,0.85", "Americana,0.85", //...esta lista tomará estos valores
                            "La Reveza,0.85", "El Cairo,1.10", "Colon,1.10",
                            "15 de Agosto,1.35"];
                        dataDestino = venta.SeparadorDestinosCostos("Vinces", destinos); // Se los manda para separar y unir con su origen
                        venta.presentarOptionsDestino(dataDestino);
                    } else {
                        let destinos = ["Playas,0.60", "Posa Seca,0.75", "Estero Medio,1",
                            "Vinces,1.35"];
                        dataDestino = venta.SeparadorDestinosCostos("15 de Agosto", destinos);
                        venta.presentarOptionsDestino(dataDestino);
                    }

                    if (venta.datos.bus > 0) {
                        $destin.removeAttribute("disabled");
                        document.querySelector('#inputPasajero').removeAttribute("disabled");
                        document.querySelector('#idModoPago').removeAttribute("disabled");
                    }

                } else {
                    document.getElementById('idCosto').value = "$" + " 0.00";
                    $destin.innerHTML = '<option value="">----</option>'
                    $destin.setAttribute("disabled", "true");
                }


            } else if (evt.target.matches("#idDestino")) { // Genera el valor para el costo del pasaje según el destino
                let costInstan = document.getElementById('idCosto');
                let destino = $destin.options[$destin.selectedIndex].value;
                if (destino != "") {
                    let item = dataDestino.find(d => d.name == destino); //Itero para encontrar aquel valor IGUAL al destino atrapado del select
                    costInstan.value = "$ " + item.costo
                } else {
                    document.getElementById('idCosto').value = "$" + " 0.00"
                }

            }
        })


        document.addEventListener('click', (evt) => {
            if (evt.target.matches("#btnDeleteRuta")) { // Permite seleccionar y deseleccionar el select de ruta
                if (venta.datos.boleto.length > 0) {
                    alert('No puedes cambiar de destino, ya hay boletos para este bus!');
                } else {
                    let variables = ['#cboRuta', '#colRuta', '#colBtnRuta', '#btnDeleteRuta'];
                    venta.DeshabilitarPasaje(variables, $destin);
                }
            }

            if (evt.target.matches("#btnDeleteBus")) { // Permite seleccionar y deseleccionar el select de bus
                if (venta.datos.boleto.length > 0) {
                    alert('No puedes quitar la selección porque ya hay boletos para este bus!');
                } else {
                    let variables = ['#cboBus', '#colBus', '#colBtnBus', '#btnDeleteBus'];
                    venta.DeshabilitarPasaje(variables, $destin);
                    venta.datos.bus = 0;
                    venta.capacidad = 0;
                }
            }

            if (evt.target.matches("#btnAgg")) { // Lógica para agregar un boleto a la tabla
                let fechaboleto = new Date;
                let ruta = $rutas.options[$rutas.selectedIndex].value; // Atrapamos la ruta
                let pasajero = document.getElementById('inputPasajero').value; // Atrapamos al pasajero
                let asiento = parseInt(document.getElementById('idAsiento').value); // Atrapamos el num de asiento
                let destino = $destin.options[$destin.selectedIndex].value; // Atrapamos el destino
                let $modoPag = document.getElementById('idModoPago'); // Atrapamos el select de modo de Pago
                let modoPago = $modoPag.options[$modoPag.selectedIndex].text; // Atrapamos el texto que contiene el modo de pago
                let hora = fechaboleto.toLocaleString(); // Genera una fecha y hora del momento actual
                if (ruta != "" && venta.datos.bus > 0) { // Siempre que haya una ruta y un bus seleccionado entrará
                    if (pasajero && asiento && destino) { // Si existen esas 3 variables entrará
                        let costoBol = dataDestino.find(d => d.name == destino); // Buscamos en los datos y preguntamos por el costo del boleto de ese destino
                        if (asiento <= venta.capacidad) { // Siempre que no se haya llegado a la capacidad del bus, se seguirán añadiendo boletos
                            let datos = {}; // Aquí iremos guardando las variables de abajo para la estructura del boleto
                            datos.id = venta.datos.boleto.length + 1; // Creamos el id con respecto a la cantidad de boletos que haya
                            datos.pasajero = pasajero;
                            datos.asiento = asiento;
                            // Aquí reemplazamos la coma de la fecha por un vacío ejem: '2/3/2023, 21:13:05' ==> '2/3/2023 21:13:05'
                            datos.hora = hora.replaceAll(',', '');
                            datos.destino = destino;
                            datos.modoPago = modoPago;
                            datos.costo = costoBol.costo;
                            venta.aggDetalleVenta(datos);

                            //Reseteo del pasaje
                            document.getElementById('inputPasajero').value = "";
                            document.getElementById('idDestino').value = "";
                            document.getElementById('idCosto').value = "$ 0.00";


                            if (asiento == venta.capacidad) { // Al vender todos los boletos o alcanzar la capacidad del bus se bloqueará los ingresos de pasaje
                                document.getElementById('inputPasajero').setAttribute('disabled', 'true');
                                document.getElementById('idDestino').setAttribute('disabled', 'true');
                                document.getElementById('idCosto').value = "$ 0.00";
                                document.getElementById('idAsiento').value = venta.capacidad;
                                document.getElementById('idModoPago').setAttribute('disabled', 'true');
                                alert('Haz vendido el último boleto, ya no puedes vender más!');
                            }
                        }
                        // }
                    } else {
                        alert('Ingrese todos los valores del pasaje!');
                    }
                } else if (ruta == "" && venta.datos.bus == 0) {
                    alert('Por favor, escoja una ruta y un bus!');
                } else if (ruta == "" && venta.datos.bus > 0) {
                    alert('Por favor, escoja una ruta!');
                } else {
                    alert('Por favor, escoja un bus!');
                }
            } else {
                if (evt.target.matches('#btnGuardar')) { // Aquí es donde se pone chido, se manda a registrar
                    if (venta.datos.boleto.length > 0) { // Siempre que hayan más de 1 boleto se procederá a registrar.
                        venta.ban = true
                        evt.preventDefault(); // Con esta función de preventDefault evitamos que se mande el form,
                        // es decir lo pausamos para tomar los otros valores faltantes.
                        venta.registroVenta();
                    } else {
                        evt.preventDefault();
                        alert("No puede guardar una venta sin ningún boleto vendido!")
                    }
                }
            }
        });


    }
)

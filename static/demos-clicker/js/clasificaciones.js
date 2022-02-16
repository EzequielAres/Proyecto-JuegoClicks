    function tablaJugadores(datos) {
        console.log(datos);
        let div = document.getElementById("padre");

        while ( div.childNodes.length >= 1 ) {
            div.removeChild( div.firstChild );
        }

        let table = document.createElement("table");
        div.appendChild(table)

        let tr = document.createElement("tr");
        let td1 = document.createElement("td");
        let td2 = document.createElement("td");
        let td3 = document.createElement("td");

        td1.innerHTML = "Nombre del jugador";
        td2.innerHTML = "Puntos";
        td3.innerHTML = "Imagen";

        td3.classList.add("encabezado");
        td1.classList.add("encabezado");
        td2.classList.add("encabezado");

        tr.appendChild(td3);
        tr.appendChild(td1);
        tr.appendChild(td2);
        table.appendChild(tr);

        for (jugador in datos) {
            let tr = document.createElement("tr");
            let td3 = document.createElement("td");
            let imagen = document.createElement("img");
            let td1 = document.createElement("td");
            let td2 = document.createElement("td");

            imagen.setAttribute("src", datos[jugador]["imagen"]);

            td1.classList.add("letrasTabla");
            td2.classList.add("letrasTabla");
            imagen.classList.add("imagenes");

            td3.appendChild(imagen);

            td1.innerHTML = datos[jugador]["username"];
            td2.innerHTML = datos[jugador]["puntos"];

            tr.appendChild(td3);
            tr.appendChild(td1);
            tr.appendChild(td2);
            table.appendChild(tr);
        }

    }

    function peticionJugadores() {
         $.ajax({
            url: 'http://localhost:5000/api/player/points',
            dataType: 'json',
            contentType: 'application/json',
            type: 'GET',
            headers: {'Authorization': 'Bearer ' + jwt},
            crossDomain: true,
            success: function(datos) { tablaJugadores(datos); }
        });
    }

    function tablaEquipos(datos) {
        console.log(datos);
        let div = document.getElementById("padre");

        while ( div.childNodes.length >= 1 ) {
            div.removeChild( div.firstChild );
        }

        let table = document.createElement("table");
        div.appendChild(table)

        let tr = document.createElement("tr");
        let td3 = document.createElement("td");
        let imagen = document.createElement("img");
        let td1 = document.createElement("td");
        let td2 = document.createElement("td");

        td3.innerHTML = "Imagen";
        td1.innerHTML = "Nombre del equipos";
        td2.innerHTML = "Puntos";

        td3.classList.add("encabezado");
        td1.classList.add("encabezado");
        td2.classList.add("encabezado");

        tr.appendChild(td3);
        tr.appendChild(td1);
        tr.appendChild(td2);
        table.appendChild(tr);

        for (equipo in datos) {
            let tr = document.createElement("tr");
            let td3 = document.createElement("td");
            let imagen = document.createElement("img");
            let td1 = document.createElement("td");
            let td2 = document.createElement("td");

            imagen.setAttribute("src", datos[equipo]["imagen"]);

            td1.classList.add("letrasTabla")
            td2.classList.add("letrasTabla")
            imagen.classList.add("imagenes");

            td3.appendChild(imagen);

            td1.innerHTML = equipo;
            td2.innerHTML = datos[equipo]['puntos'];

            tr.appendChild(td3);
            tr.appendChild(td1);
            tr.appendChild(td2);
            table.appendChild(tr);
        }

    }

    function peticionEquipos() {
         $.ajax({
            url: 'http://localhost:5000/api/team/points',
            dataType: 'json',
            contentType: 'application/json',
            type: 'GET',
            headers: {'Authorization': 'Bearer ' + jwt},
            crossDomain: true,
            success: function(datos) { tablaEquipos(datos); }
        });
    }

    function tablaLocations(datos) {
        console.log(datos);
        let div = document.getElementById("padre");

        while ( div.childNodes.length >= 1 ) {
            div.removeChild( div.firstChild );
        }

        let table = document.createElement("table");
        div.appendChild(table)

        let tr = document.createElement("tr");
        let td1 = document.createElement("td");
        let td2 = document.createElement("td");

        td1.innerHTML = "Nombre de la localidad";
        td2.innerHTML = "Puntos";

        td1.classList.add("encabezado")
        td2.classList.add("encabezado")

        tr.appendChild(td1);
        tr.appendChild(td2);
        table.appendChild(tr);

        for (localidad in datos) {
            let tr = document.createElement("tr");
            let td1 = document.createElement("td");
            let td2 = document.createElement("td");

            td1.classList.add("letrasTabla")
            td2.classList.add("letrasTabla")

            td1.innerHTML = localidad;
            td2.innerHTML = datos[localidad];

            tr.appendChild(td1);
            tr.appendChild(td2);
            table.appendChild(tr);
        }

    }

    function peticionLocations() {
         $.ajax({
            url: 'http://localhost:5000/api/location/points',
            dataType: 'json',
            contentType: 'application/json',
            type: 'GET',
            headers: {'Authorization': 'Bearer ' + jwt},
            crossDomain: true,
            success: function(datos) { tablaLocations(datos); }
        });
    }

    function tablaRegions(datos) {
        console.log(datos);
        let div = document.getElementById("padre");

        while ( div.childNodes.length >= 1 ) {
            div.removeChild( div.firstChild );
        }

        let table = document.createElement("table");
        div.appendChild(table)

        let tr = document.createElement("tr");
        let td1 = document.createElement("td");
        let td2 = document.createElement("td");

        td1.innerHTML = "Nombre de la región";
        td2.innerHTML = "Puntos";

        td1.classList.add("encabezado")
        td2.classList.add("encabezado")

        tr.appendChild(td1);
        tr.appendChild(td2);
        table.appendChild(tr);

        for (region in datos) {
            let tr = document.createElement("tr");
            let td1 = document.createElement("td");
            let td2 = document.createElement("td");

            td1.classList.add("letrasTabla")
            td2.classList.add("letrasTabla")

            td1.innerHTML = region;
            td2.innerHTML = datos[region];

            tr.appendChild(td1);
            tr.appendChild(td2);
            table.appendChild(tr);
        }

    }

    function peticionRegions() {
         $.ajax({
            url: 'http://localhost:5000/api/region/points',
            dataType: 'json',
            contentType: 'application/json',
            type: 'GET',
            headers: {'Authorization': 'Bearer ' + jwt},
            crossDomain: true,
            success: function(datos) { tablaRegions(datos); }
        });
    }

    function tablaCountries(datos) {
        console.log(datos);
        let div = document.getElementById("padre");

        while ( div.childNodes.length >= 1 ) {
            div.removeChild( div.firstChild );
        }

        let table = document.createElement("table");
        div.appendChild(table)

        let tr = document.createElement("tr");
        let td1 = document.createElement("td");
        let td2 = document.createElement("td");

        td1.innerHTML = "Nombre del país";
        td2.innerHTML = "Puntos";

        td1.classList.add("encabezado")
        td2.classList.add("encabezado")

        tr.appendChild(td1);
        tr.appendChild(td2);
        table.appendChild(tr);

        for (country in datos) {
            let tr = document.createElement("tr");
            let td1 = document.createElement("td");
            let td2 = document.createElement("td");

            td1.classList.add("letrasTabla")
            td2.classList.add("letrasTabla")

            td1.innerHTML = country;
            td2.innerHTML = datos[country];

            tr.appendChild(td1);
            tr.appendChild(td2);
            table.appendChild(tr);
        }

    }

    function peticionCountries() {
         $.ajax({
            url: 'http://localhost:5000/api/country/points',
            dataType: 'json',
            contentType: 'application/json',
            type: 'GET',
            headers: {'Authorization': 'Bearer ' + jwt},
            crossDomain: true,
            success: function(datos) { tablaCountries(datos); }
        });
    }
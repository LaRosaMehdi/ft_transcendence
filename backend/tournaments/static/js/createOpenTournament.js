document.addEventListener('DOMContentLoaded', function() {
    var tableBody = document.getElementById('results-body');
    var currentUser = document.getElementById('tournament-results').getAttribute('data-current-user');

    // Fonction pour remplir la table avec les joueurs
    function fillTable(players) {
        tableBody.innerHTML = ''; // Effacer le contenu précédent
        players.forEach(function(player, index) {
            var row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${player.username}</td>
                <td>${player.victoires}</td>
                <td>${player.nulles}</td>
                <td>${player.defaites}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    // Envoi d'une requête AJAX pour récupérer les joueurs du tournoi public
   // fetch('/tournament/getPublicPlayers/')
   //     .then(response => response.json())
   //     .then(data => {
   //         console.log('Joueurs récupérés avec succès:', data);
   //         fillTable(data.players); // Remplir la table avec les joueurs récupérés
   //     })
   //     .catch(error => {
   //         console.error('Erreur lors de la récupération des joueurs:', error);
   //     });

    // Fonction pour gérer le clic sur le bouton "Modifier"
    function modifyHandler(event) {
        event.preventDefault();
        var numPlayers = parseInt(document.getElementById('num-players').value, 10);
        console.log("Nombre de joueurs à modifier :", numPlayers);

        // Modifier les lignes du tableau pour chaque joueur
        var rows = tableBody.getElementsByTagName('tr');
        for (var i = 0; i < rows.length; i++) {
            var playerName = i === 0 ? currentUser.username : 'En attente...';
            rows[i].getElementsByTagName('td')[1].textContent = playerName;
        }

        // Envoi d'une requête AJAX pour modifier les données du tableau
        fetch('/tournoi/modify_open_tournament/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ numPlayers: numPlayers })
        })
        .then(response => {
            if (response.ok) {
                // Traitement réussi
                alert('Nombre de joueurs modifié avec succès.');
            } else {
                // Traitement échoué
                alert('Erreur lors de la modification du nombre de joueurs.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Gestion des erreurs
        });
    }

    var form = document.getElementById('player-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        tableBody.innerHTML = ''; // Effacer le contenu précédent
        var numPlayers = parseInt(document.getElementById('num-players').value, 10);
        console.log("Nombre de joueurs à générer :", numPlayers);

        // Générer les lignes du tableau pour chaque joueur
        for (var i = 0; i < numPlayers; i++) {
            var playerName = i === 0 ? currentUser.username : 'En attente...';
            var player = {
                position: i + 1,
                name: playerName,
                wins: 0,
                draws: 0,
                losses: 0
            };
            console.log("Joueur à ajouter :", player);
            var row = document.createElement('tr');
            row.innerHTML = `
                <td>${player.position}</td>
                <td>${player.name}</td>
                <td>${player.wins}</td>
                <td>${player.draws}</td>
                <td>${player.losses}</td>
            `;

            console.log("Ligne du tableau :", row.innerHTML);
            tableBody.appendChild(row);
        }
        // Après la boucle for qui génère les lignes du tableau
        var generateButton = document.getElementById('generate-button');
        generateButton.textContent = 'Modifier';
        generateButton.addEventListener('click', modifyHandler); // Ajouter un nouveau gestionnaire d'événement
    });
});

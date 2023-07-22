let bestellenButtons = document.getElementsByClassName("warenkorb-bestellen");

for (let i = 0; i < bestellenButtons.length; i++) {
    bestellenButtons[i].addEventListener('click', function(){
        let artikelID = this.dataset.artikel;
        let action = this.dataset.action;
        
        if(benutzer == 'AnonymousUser'){
            updateGastBestellung(artikelID, action)
        } else {
            updateKundenBestellung(artikelID, action)
        }
    })    
}

function updateGastBestellung(artikelID, action){
    if(action == 'bestellen'){
        if(warenkorb[artikelID] == undefined){
            warenkorb[artikelID] = {'menge':1}
        } else {
            warenkorb[artikelID]['menge'] +=1
        }
    }
    if(action == 'entfernen'){
        warenkorb[artikelID]['menge'] -=1

        if(warenkorb[artikelID]['menge'] <=0) {
            delete warenkorb[artikelID]
        }
    }
    document.cookie = 'warenkorb=' + JSON.stringify(warenkorb) + ";domain;path=/; SameSite=None; Secure"
    console.log(warenkorb)
    location.reload()
}

function updateKundenBestellung(artikelID, action){
    let url = "/artikel_backend/";

    fetch(url, {
        method: 'post',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify ({'artikelID':artikelID, 'action': action})
    })
    .then(()=>location.reload())
}

// Kasse
let formular = document.getElementById('formular')
let gesamtpreis = document.getElementById('gesamtpreis').value

formular.addEventListener('submit', function(e){
    e.preventDefault()
    document.getElementById('formular-button').classList.add('d-none');
    document.getElementById('bezahlen-info').classList.remove('d-none');
})

document.getElementById('bezahlen-button').addEventListener('click', function(e){
    submitFormular()
})

function submitFormular() {
    let benutzerDaten = {
        'name': formular.inputName.value,
        'email': formular.inputEmail.value,
        'gesamtpreis': gesamtpreis,
    }
    let lieferAdresse = {
        'Adresse': formular.inputAdresse.value,
        'plz': formular.inputPlz.value,
        'stadt': formular.inputStadt.value,
        'land': formular.inputLand.value,
    }
    console.log(benutzerDaten, lieferAdresse)

    let url = "/bestellen/";

    fetch(url, {
        method: 'post',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify ({'benutzerDaten':benutzerDaten, 'lieferAdresse': lieferAdresse})
    })
    .then(()=>window.location.href="/")
}
let bestellenButtons = document.getElementsByClassName("warenkorb-bestellen");

for (let i = 0; i < bestellenButtons.length; i++) {
    bestellenButtons[i].addEventListener('click', function(){
        let artikelID = this.dataset.artikel;
        let action = this.dataset.action;
        updateKundenBestellung(artikelID, action)
    })
    
}

function updateKundenBestellung(artikelID, action){
    let url = "/artikel_backend/";

    fetch(url, {
        method: 'post',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify ({'artikelID':artikelID, 'action': action})
    })
}
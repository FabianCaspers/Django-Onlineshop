let bestellenButtons = document.getElementsByClassName("warenkorb-bestellen");

for (let i = 0; i < bestellenButtons.length; i++) {
    bestellenButtons[i].addEventListener('click', function(){
        let artikelID = this.dataset.artikel;
        let action = this.dataset.action;
        
    })
    
}
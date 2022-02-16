class Game1 {
    constructor(player) {
        this.player = player;
        this.clicks = 10;
        $("#timer").text(this.clicks);
    }

    randomRectangle() {
        const margin = 1;
        const maxwidth = 12;
        const maxheight = 12;
        var x = margin + Math.random()*(100-margin*2-maxwidth);
        var y = margin + Math.random()*(100-margin*2-maxheight);
        var width = 3+Math.random()*maxwidth;
        var height = 3+Math.random()*maxheight;
        $("#rectangle").css("width", width+"%");
        $("#rectangle").css("height", height+"%");
        $("#rectangle").css("top", x+"%");
        $("#rectangle").css("left", y+"%");
    }

    updateClicks() {
        $.ajax({
            url: 'http://localhost:5000/api/player/' + player,
            dataType: 'json',
            contentType: 'application/json',
            type: 'GET',
            headers: {'Authorization': 'Bearer ' + jwt},
            crossDomain: true,
            success: this.setClicks
        });
    }

    setClicks(data) {
        debugger
        document.title = data['username'] + " -> " + data['puntos'] + " v0.1";
        $("#player").text(data['username']);
        $("#clicks").text(data['puntos']);
    }

    click() {
        this.clicks -= 1;
        if(this.clicks==0) {
            this.clicks = 10;
            this.addClicks(10);
            this.randomRectangle();
        }
        $("#timer").text(this.clicks);
    }

    addClicks(n) {
        var data = JSON.stringify({"clicks" : n });
        $.ajax({
            url: 'http://localhost:5000/api/player/points/'+ player,

            dataType: 'json',
            contentType: 'application/json',
            type: 'POST',
            data: data,
            headers: {'Authorization': 'Bearer ' + jwt},
            crossDomain: true,
            success: this.setClicks,

        });
    }
}
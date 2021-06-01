class BoggleGame {
    constructor(Id, time = 60) {
        this.board = $('#' + Id)
        this.words = new Set();
        this.score = 0

        this.time = time
        this.showTimer()

        this.timer = setInterval(this.clock.bind(this), 1000)

        //handleSubmit gets current value and adds to list
        //"perma-binding" this to work as a callback
        $('.form', this.board).on('submit', this.handleSubmit.bind(this))
        
    }


    //shows score
    showScore() {
        $('.score', this.board).text(this.score)
    }

    //shows message
    showMessage(message, status) {
        $('.msg', this.board).text(message).removeClass().addClass(`msg ${status}`)
    }

    //handleSubmit to validate word
    async handleSubmit(e){
        e.preventDefault();

        const $word = $('.guess', this.board)

        let word = $word.val()
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`Already found "${word}", try again`, 'error')
            return;
        }

        //making an AJAX request to check validity of word from server
        const res = await axios.get('/check-word', {params: {word:word}})
        if (res.data.result === "not-word") {
            this.showMessage(`"${word}" is not a valid word`, "error")
        } else if (res.data.result === "not-on-board") {
            this.showMessage(`"${word}" is not a valid word on the board`, "error")
        } else {
            this.score += word.length
            this.showScore()
            this.words.add(word)
            this.showMessage(`"${word}" is valid!`, "success")
        } 
        $word.val('')
    }

    //Timer
    showTimer() {
        $('.timer', this.board).text(this.time)
    }


    async clock() {
        this.time -= 1
        this.showTimer()

        if (this.time === 0) {
            clearInterval(this.timer)
            await this.scoreGame();
        }
    }

    //end of game showing score and display message
    async scoreGame() {
        $('.form', this.board).hide()
        const res = await axios.post('/score', { score:this.score})
        if (res.data.newHighScore) {
            this.showMessage(`New High Score of ${this.score} points!`, "final")
        } else {
            this.showMessage(`Final Score: ${this.score} points`, "final")
        }
    }
    
    
}    
//  function to launch a game
window.launchGame = function() {
    console.log("Play Game button clicked!");
    fetch('/start-game')
        .then(response => response.json())
        .then(data => {
            console.log("Server Response:", data.message);
        })
        .catch(error => console.error('Error launching game:', error));
};

window.exitToDesktop = function() {
    if (confirm("Are you sure you want to Quit?")) {
        window.close();
        
    }
};
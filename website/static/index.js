function copyToClipboard(contentId) {
    var copyText = document.getElementById('dkim' + contentId).innerText;
    navigator.clipboard.writeText(copyText).then(() => {
        // Alert the user that the action took place.
        // Nobody likes hidden stuff being done under the hood!
        document.getElementById('bdkim' + contentId).innerText = 'Zkopírováno!'
        document.getElementById('bdkim' + contentId).className = 'btn btn-success';
        setTimeout(() => {
            document.getElementById('bdkim' + contentId).innerText = 'Zkopírovat DKIM';
            document.getElementById('bdkim' + contentId).className = 'btn btn-secondary';
        }, 2000);
    });
}